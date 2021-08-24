import jwt

from datetime import datetime, timedelta

from server.Database import Mongo
from server.Models.Teams.Teams import TeamsModel

from server.config import Configuration




class TeamsManager:
    def __init__(self, name=None):
        self.db = Mongo.teams
        self.team = TeamsModel(name)

    def __enter__(self):
        # self.session = Mongo.start_session()  <- mongodb mutex lock
        result = self.find_team()
        if result:
            self.team.set_name(result['name'])
            self.team.set_members(result['members'])
            self.team.set_submission_id(result['submission_id'])
            self.team.set_last_submission_timestamp(result['last_submission'])
            self.team.set_created_timestamp(result['created_timestamp'])
            self.found = True
        else:
            self.found = False
        return self

    def __exit__(self, type, value, tb):
        # self.session.end_session()  <- mongodb mutex unlock
        pass

    def find_team(self):
        pass

    def commit(self):
        pass
