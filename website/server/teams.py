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
    NOT_INVITED_ERROR = 6

    def __init__(self, client, database,input_session = None):
        self.client = client
        self.database = database
        self.error = None
        if input_session:
            self.session = input_session
        else:
            self.session = self.client.start_session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.session.end_session()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False
        return True

    def can_invite(self, sender_username, recipient_username):
        """Returns true if the user can send an invite to the recipient."""
        sender_team = self.get_user_team(sender_username)
        if sender_team == None:
            return self.INVALID_TEAM_ERROR
        elif sender_team['user_count'] == self.MAX_TEAM_USER_COUNT:
            return self.TEAM_MAX_CAPACITY_ERROR
        elif self.get_user_team(recipient_username) != None:
            return self.USER_ON_TEAM_ERROR
        return 0

    def send_invite(self, sender_username, recipient_username):
        '''Sends an invite from recipient user to sender user.'''
        session = self.session
        try:
            session.start_transaction()
            invite_validity = self.can_invite(
                sender_username, recipient_username)
            if invite_validity != 0:
                self.error = invite_validity
                return False
            sender_team = self.get_user_team(sender_username)
            if "name" not in sender_team:
                self.error = self.INVALID_TEAM_ERROR
                return False
            sender_team_name = sender_team["name"]
            # Add to list of invites on recipient user
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
            # Add user list of invited users on team
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
            if team_result.modified_count != 1:
                self.session.abort_transaction()
                self.error = self.INVITE_EXISTS_ERROR
                return False
            session.commit_transaction()
        except (Exception) as exc:
            traceback.print_exc()
            session.abort_transaction()
            return False
        return True

    def _can_accept(self, username, team_name):
        """
        Returns 0 iff the user is able to accept.
        Returns USER_ON_TEAM_ERROR if user is already on a team.
        Returns INVALID_TEAM_ERROR if the team accepting invite from 
        does not exist.
        """
        user_team = self.get_user_team(username)
        goal_team = self.get_team(team_name)
        if user_team != None:
            return self.USER_ON_TEAM_ERROR
        elif not goal_team:
            return self.INVALID_TEAM_ERROR
        elif goal_team['user_count'] >= self.MAX_TEAM_USER_COUNT:
            return self.TEAM_MAX_CAPACITY_ERROR
        elif not "invites" in goal_team or not username in goal_team["invites"]: 
            return self.NOT_INVITED_ERROR
        return 0

    def accept_invite(self, username, team_name):
        ''' Joins team through an invite received.
            Returns Error if accept could not be performed.
            Returns 0 otherwise.
        '''
        session = self.session
        try:
            session.start_transaction()
            can_accept = self._can_accept(username, team_name)
            if can_accept != 0:
                self.error = can_accept
                return False
            # Add the user to the team
            team_data = {
                "$push": {"users": username},
                "$pull": {"invites": username},
                "$inc": {"user_count": 1}, }
            team_query = {'name': team_name,
                          "users": {"$nin": [username]},
                          "user_count": {"$lt": self.MAX_TEAM_USER_COUNT}
                          }
            team_result = self.database.teams.update_one(
                team_query,
                team_data,
                session=session
            )
            if team_result.modified_count != 1:
                self.error = self.INVALID_TEAM_ERROR
                return False

           # Add the team to the user if possible

            user_query = {'username': username, "$or": [
                {"team": {"$exists": False}}, {"team": {"$eq": ""}}, ], }
            user_data = {"$set":{"team": team_name},
                "$pull": {"invites":team_name}}
            user_result = self.database.users.update_one(
                user_query,
                user_data,
                session=session
            )
            if user_result.modified_count != 1:
                self.error = self.USER_ON_TEAM_ERROR
                return False
            session.commit_transaction()
        except (Exception) as exc:
            print(exc)
            session.abort_transaction()
            return False
        return True

    def is_valid_team_name(self, teamName):
        return len(teamName) < 16 and len(teamName) > 4

    '''
        Safely creates a team for a user.
        Returns false if the user is already on a team.
    '''

    def create_team(self, username, displayName):
        displayName = displayName.strip()

        team_name = displayName.lower().strip()
        if self.get_user_team(username) != None or not self.is_valid_team_name(team_name):
            self.error = self.USER_ON_TEAM_ERROR
            return False
        if self.database.teams.find_one({"name": team_name}) != None:
            self.error = self.TEAM_EXISTS_ERROR
            return False

        session = self.session
        try:
            session.start_transaction()
            team_data = {
                "name": team_name,
                "displayName": displayName,
                "users": [username],
                "user_count": 1,
                "invites": [],
                "creator": username
            }
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
            user_query = {'username': username, "$or": [
                {"team": {"$exists": False}}, {"team": {"$eq": ""}}, ], }
            user_data = {"team": team_name}
            user_result = self.database.users.update_one(
                user_query,
                {"$set": user_data},
                session=session
            )
            if user_result.modified_count != 1:
                self.session.abort_transaction()
                self.error = self.USER_ON_TEAM_ERROR
                return False
            session.commit_transaction()
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
        team_name = team["name"]

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
                session=session
            )
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
                session=session
            )
            if user_result.modified_count != 1:
                self.session.abort_transaction()
                self.error = self.INVALID_TEAM_ERROR
                return False

            session.commit_transaction()
        except (Exception) as exc:
            print(exc)
            session.abort_transaction()
            return False
        return True

    def get_user_team(self, username):
        '''
        Returns None if the user has no team, returns the team object otherwise.
        '''
        user_file = self.database.users.find_one(
            {"username": username}, session=self.session)
        if 'team' not in user_file or user_file['team'] == '':
            return None
        team_document = self.database.teams.find_one(
            {'name': user_file['team']}, session=self.session)
        return team_document

    def get_team(self, team_name):
        ''' Gets the team document for a given team_name'''
        team_document = self.database.teams.find_one(
            {'name': team_name}, session=self.session)
        return team_document

    def get_user_invites(self, username):
        '''Gets the invites received by a given user'''
        user_file = self.database.users.find_one(
            {"username": username}, session=self.session)
        if "invites" not in user_file:
            return {}
        invite_list = user_file["invites"]
        ret = {}
        for team in invite_list:
            temp_team = self.database.teams.find_one(
                {"name": team}, session=self.session)
            ret[temp_team["name"]] = temp_team["displayName"]
        return ret
