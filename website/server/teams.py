from pymongo import MongoClient
from flask import Flask, jsonify, send_from_directory, request, abort, session
from flask_cors import CORS
import traceback
'''
Performs all Teams-related logic with Database.
'''


class TeamController:
    MAX_TEAM_USER_COUNT = 4
    # TeamController Errors
    TEAM_EXISTS_ERROR = 1
    USER_ON_TEAM_ERROR = 2
    INVALID_TEAM_ERROR = 3
    TEAM_MAX_CAPACITY_ERROR = 4
    INVITE_EXISTS_ERROR = 5

    def __init__(self, client, database):
        self.client = client
        self.database = database
        self.error = None

    def __enter__(self):
        self.session = self.client.start_session()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.session.end_session()
        self.session = None
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            # return False # uncomment to pass exception through
            session.end_session()
            return False
        return True

    def can_invite(self, sender_username, recipient_username):
        """Returns true if the user can send an invite to the recipient."""
        sender_team = self.get_user_team(sender_username)
        # Transaction safety
        if sender_team == None:
            return self.INVALID_TEAM_ERROR
        elif sender_team['user_count'] == self.MAX_TEAM_USER_COUNT:
            return self.TEAM_MAX_CAPACITY_ERROR
        elif self.get_user_team(recipient_username) != None:
            return self.USER_ON_TEAM_ERROR
        return 0

    def send_invite(self, recipient_username, sender_username):
        '''Sends an invite from recipient user to sender user.'''
        session = self.session
        try:
            session.start_transaction()
            # Transaction safety
            invite_validity = self.can_invite(sender_username, recipient_username)
            if invite_validity != 0:
                self.error = invite_validity
                return False
            sender_team = self.get_user_team(sender_username)
            if "name" not in sender_team:
                self.error = INVALID_TEAM_ERROR
                return False
            sender_team_name = sender_team["name"]
            # add to list of invites on recipient user
            recipient_query = {'username': recipient_username,
                "$or": [
                {"team": {"$exists": False}}, {"team": {"$eq": ""}}, ],
                "invites": {"$nin": [sender_team_name]}
            }
            recipient_data = {
                "$push": {"invites": sender_team_name}
            }
            user_result = self.database.users.update_one(
                recipient_query,
                recipient_data,
                session=self.session
            )
            if user_result.modified_count != 1:
                self.session.abort_transaction()
                self.error = self.INVITE_EXISTS_ERROR
                return False
            print("Didn't reach here")
            # add user list of invited users on team
            team_query = {'name': sender_team_name,
                        'user_count': {'$lt': self.MAX_TEAM_USER_COUNT + 1}
                        }
            team_data = {"$push": {"invites": recipient_username}}
            team_result = self.database.teams.update_one(
                team_query,
                team_data,
                upsert=True,
                session=session
            )
            print("Didn't reach here")
            if team_result.modified_count != 1:
                self.session.abort_transaction()
                self.error = self.INVITE_EXISTS_ERROR
                return False
            session.commit_transaction()
            print("Successfully invited user to team.")
        except (Exception) as exc:
            print(exc)
            session.abort_transaction()
            return False
        return True


    def _can_accept(self, username):
        """
        Returns True iff the user is able to accept.
        """
        team = self.get_user_team(sender_username)
        if team == None:
            return False
        # if len(team['members']) == self.MAX_TEAM_MEMBERS:
        #     return False  # abort(403)
        # if self.get_user_team(recipient_username) != None:
        #     return False  # abort(403)
        return True

    def accept(self, username, teamName):
        '''
            # Transaction safety
            Joins team through an invite received.
            Returns False if accept could not be performed.
            Returns true otherwise.
        '''
        if not self._can_accept(username):
            return False
        team = self.database.teams.find_one({'name': teamName.lower()})
        if team != null:
            return False

        self.database.teams.update_one(team)
        user = self.database.users.find_one({'username': username})
        self.database.users.update_one({'username'})
        return True

    def is_valid_team_name(self, teamName):
        return len(teamName) > 8

    '''
        Safely creates a team for a user.
        Returns false if the user is already on a team.
    '''
    def create_team(self, username, displayName):
        team_name = displayName.lower().strip()
        if self.get_user_team(username) != None or not self.is_valid_team_name(team_name):
            self.error = self.USER_ON_TEAM_ERROR
            return False
        if self.database.teams.find_one({"name": team_name}) != None:
            self.error = self.TEAM_EXISTS_ERROR
            return False

        # Start the session for transaction
        session = self.session
        try:
            session.start_transaction()
            team_data = {"name": team_name,
                         "displayName": displayName, "users": [username], "user_count": 1}
            team_query = {'name': team_name}
            team_result = self.database.teams.update_one(
                team_query,
                {"$setOnInsert": team_data},
                upsert=True,
                session=session
            )
            if not team_result.upserted_id:
                self.session.abort_transaction()
                self.error = self.TEAM_EXISTS_ERROR
                return False
            user_query = {'username': {"$eq": username}, "$or": [
                {"team": {"$exists": False}}, {"team": {"$eq": ""}}, ], }
            user_data = {"team": team_name}
            user_result = self.database.users.update_one(
                user_query,
                {"$set": user_data},
                session=self.session
            )
            if user_result.modified_count != 1:
                self.session.abort_transaction()
                self.error = self.USER_ON_TEAM_ERROR
                return False
            session.commit_transaction()
            print("Create Team Transaction success.")
        except (Exception) as exc:
            print(exc)
            session.abort_transaction()
            return False
        return True

    '''
        Removes user with username from their current team.
        Returns False on failure,
        Returns True on success.
    '''
    def leave_team(self, username):
        team = self.get_user_team(username)
        if team == None:
            self.error = self.INVALID_TEAM_ERROR
            return False
        print("User is on team:", str(team))
        team_name = team["name"]

        # Start the session for transaction
        session = self.session
        try:
            session.start_transaction()
            team_data = {
                "$pull": {"users": username},
                "$inc": {"user_count": -1}, }
            team_query = {'name': team_name,
                          "users": username}
            team_result = self.database.teams.update_one(
                team_query,
                team_data,
                upsert=True,
                session=session
            )
            print("Removed user from team object")
            if team_result.modified_count != 1:
                self.session.abort_transaction()
                self.error = self.INVALID_TEAM_ERROR
                return False

            user_query = {'username': username,
                          "team": team_name}
            user_data = {"team": ""}
            user_result = self.database.users.update_one(
                user_query,
                {"$set": user_data},
                session=self.session
            )
            if user_result.modified_count != 1:
                self.session.abort_transaction()
                self.error = self.INVALID_TEAM_ERROR
                return False
            print("Removed team from user object")

            session.commit_transaction()
            print("Leaving Team Transaction success.")
        except (Exception) as exc:
            print(exc)
            session.abort_transaction()
            return False
        return True

    '''
    Returns None if the user has no team, returns the team object otherwise.
    '''

    def get_user_team(self, username):
        user_file = self.database.users.find_one(
            {"username": username}, session=self.session)
        if 'team' not in user_file or user_file['team'] == '':
            return None
        team_document = self.database.teams.find_one(
            {'name': user_file['team']}, session=self.session)
        print("Got user team")
        return team_document
