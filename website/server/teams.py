from pymongo import MongoClient
from flask import Flask, jsonify, send_from_directory, request, abort, session
from flask_cors import CORS

'''
Performs all Teams-related logic with Database.
'''


class TeamsController:
    MAX_TEAM_MEMBERS = 4

    def __init__(self, username, teamname):
        self.username = username
        self.teamname = teamname


    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def set_db_client(self, database_client):
        self.database_client = database_client

    def is_valid_team_name(self):
        return len(self.teamname) > 8

    '''
    Returns None if the user has no team, returns the team object otherwise.
    '''
    def get_user_team(self, teamCollection, userCollection):
        # login_guard()
        user_file=userCollection.find_one({"username": self.username})
        if 'team' not in user_file or user_file['team'] == '':
            print("returning none")
            return None
        return teamCollection.find_one({'name': user_file['team']})

    '''
        Creates a team for a user. Returns false if the user is already on a team.
    '''
    def create_team(self):
        name = self.teamname.lower()
        session = self.database_client.start_session()
        teamCollection = session.client.get_database("deerhunt_db").teams
        userCollection = session.client.get_database("deerhunt_db").users
        if self.get_user_team(teamCollection, userCollection) != None or not self.is_valid_team_name():
            return False
        # if userCollection.find_one({"name": name}) != None:
        #     return False

        def transaction(session, teamCollection, userCollection):
            team_data = {"name": name,
                "displayName": self.teamname, "users": [self.username]}
            team_query = {'name': name}
            team_id = teamCollection.update_one(
                team_query,
                {"$setOnInsert": team_data},
                upsert=True,
                session=session
            )
            print(team_id)
            print("got here")
            user_query = {'username': self.username}
            user_data = {"team": name}
            user_id = userCollection.update_one(
                user_query, {"$set": user_data}, upsert=True
            )
            print(user_id)
        try:
            transaction(session, teamCollection, userCollection)
        except Exception:
            pass
        finally:
            session.end_session()
        return True







    '''
    Returns true if the user can send an invite to the recipient
    '''
    def can_invite(recipient_username, team):
        if team == None:
            return False
        if len(team['members']) == self.MAX_TEAM_MEMBERS:
            return False
        if get_user_team(recipient_username) != None:
            return False
        return True

    '''
    '''
    def send_invite(team, user):
        if not self.can_invite():
            return False
        # TODO: Complete sending of in

    '''
    Returns True iff the user is able to
    '''
    def _can_accept(username):
        team = self.get_user_team(sender_username)
        if team == None:
            return False  # abort(403)
        if len(team['members']) == self.MAX_TEAM_MEMBERS:
            return False  # abort(403)
        if self.get_user_team(recipient_username) != None:
            return False  # abort(403)
        return True

    '''
        Joins team through an invite received.
        Returns False if accept could not be performed.
        Returns true otherwise.
    '''
    def accept(username, teamName):
        if not self._can_accept(username):
            return False
        team = self.database.teams.find_one({'name': teamName.lower()})
        if team != null:
            return False

        self.database.teams.update_one(team)
        user = self.database.users.find_one({'username': username})
        self.database.users.update_one({'username'})
        return True


    '''
        Removes user with username from a team.
        Returns False on failure,
        Returns True on success.
    '''
    def leave_team(username):
        team = self.get_user_team(username)

        user = self.database.users.find_one({'username': username})
        if team == None:
            return False
        self.database.teams.update_one(
            {"_id": team["_id"]}, {"$pull": {"users": username}})
        self.database.user.update_one({"_id": user["_id"]}, {"team": ""})