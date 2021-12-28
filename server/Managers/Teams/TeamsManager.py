import jwt

from datetime import datetime, timedelta

from server.Database import Mongo
from server.Models.Teams.Teams import TeamsModel

from server.config import Configuration

class TeamsManager:
    def __init__(self, name, owner):
        self.db = Mongo.teams
        self.team = TeamsModel(name, owner)

    def __enter__(self):
        # self.session = Mongo.start_session()  <- mongodb mutex lock
        result = self.find_team()
        if result:
            self.team.set_members(result['members'])
            self.team.join_event(result['eventID'])
            self.team.set_last_submission_timestamp(result['last_submission'])
            self.team.set_created_timestamp(result['created_timestamp'])
            self.found = True
        else:
            self.found = False
        return self

    def __exit__(self, type, value, tb):
        # self.session.end_session()  <- mongodb mutex unlock
        pass

    def createTeam(self) -> bool:
        if not self.found:
            try:
                self.team.set_created_timestamp(str(datetime.utcnow()))
                self.commit()
                return True
            except Exception:
                return False
        else:
            return False

    def find_team(self):
        if self.team.name:
            team = self.db.find_one({'name': self.team.name})
            return team
        return None

    def is_joined_team(self):
        pass

    def commit(self):
        query = {'name': self.team.name}
        data = self.team.covert_to_dict()
        if self.found:
            self.db.update_one(query, {'$set': data })
        else:
            self.db.update_one(query, {"$setOnInsert": data}, upsert=True)
