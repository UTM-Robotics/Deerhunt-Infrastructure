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
        return self.db.find_one({'name': self.team.get_name()})
    
    def create_team(self, creator):
        if not self.found:
            self.team.set_created_timestamp(str(datetime.utcnow()))
            self.team.add_member(creator)
            # create azure container here
            self.commit()
            return True
        return False

    def commit(self):
        query = {'name': self.team.get_name()}
        data = self.team.covert_to_dict()
        if self.found:
            self.db.update_one(query, {'$set': data })
        else:
            self.db.update_one(query, {"$setOnInsert": data}, upsert=True)
