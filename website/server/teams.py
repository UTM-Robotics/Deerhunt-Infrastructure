from pymongo import MongoClient
from flask import Flask, jsonify, send_from_directory, request, abort, session
from flask_cors import CORS

'''
Performs all Teams-related logic with Database.
'''


class TeamsController:
    MAX_TEAM_MEMBERS = 4

    def __init_(self, database):
        self.database = database

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

    def is_valid_team_name(teamName):
        return True

    '''
        Creates a team for a user. Returns false if the user is already on a team.
    '''
    def create_team(username, teamName):
        if self.get_user_team(username) != None or not self.is_valid_team_name(teamName):
            return False
        name = teamName.lower()
        if self.database.teams.find_one({"name": name}) != null:
            return False
        team_id = self.database.teams.insert_one(
            {"name": name, "displayName": teamName, "users": [username]})
        query = {'username': username}
        self.database.users.update_one(query, {"team": team_id})
        return True

    '''
        Removes user with username from a team.
        Returns False on failure,
        Returns True on success.
    '''
    def leave_team(username):
        team = self.get_user_team(username)

        user = self.database.users.find_one({'username': username}})
        if team == None:
            return False
        self.database.teams.update_one(
            {"_id": team["_id"]}, {"$pull": {"users": username}})
        self.database.user.update_one({"_id": user["_id"]}, {"team": ""})

    '''
    Returns None if the user has no team, returns the team object otherwise.
    '''
    def get_user_team(username):
        login_guard()
        user_file=database.users.find_one({session['username']})
        if 'team' not in user_file or user_file['team'] == '':
            return None
        return database.teams.find_one({'_id': user_file['team']})
