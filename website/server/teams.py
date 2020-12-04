from pymongo import MongoClient
from flask import Flask, jsonify, send_from_directory, request, abort, session
from flask_cors import CORS
class Teams:
    MAX_TEAM_MEMBERS = 4
    def __init_(self, database):
        self.database = database
    
    '''
    Returns true if the user can send an invite to the recipient
    '''
    def can_invite(sender_username,recipient_username, session):
        team = get_user_team(sender_username)

        if len(team['members']) == MAX_TEAM_MEMBERS:
            abort(403)
        if get_user_team(recipient_username) != None:
            abort(403)

        return True

    '''
    '''
    def send_invite(team):
        if not can_invite():
            return False
        
    '''
    '''
    def can_accept(username):

    '''
        Joins team through an invite received.
    '''
    
    '''
    Returns None if the user has no team, returns the team object otherwise.
    '''
    def get_user_team(username):
        login_guard()
        user_file = database.users.find_one({session['username']})
        if 'team' not in user_file or user_file['team'] == '':
            None
        return database.teams.find_one({'_id': user_file[team]})
