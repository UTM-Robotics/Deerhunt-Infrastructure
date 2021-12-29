from typing import Optional
import jwt

from datetime import datetime, timedelta

from server.Database import Mongo
from server.Models.Teams.Teams import TeamsModel

from server.config import Configuration

class TeamsManager:
    def __init__(self, name):
        self.db = Mongo.teams
        self.team = TeamsModel(name)

    def __enter__(self):
        # self.session = Mongo.start_session()  <- mongodb mutex lock
        result = self.find_team()
        if result:
            self.team.set_owner(result['owner'])
            self.team.set_created_timestamp(result['created_timestamp'])
            self.pass_data(result)
            print(self.get_id())
            self.found = True
        else:
            self.found = False
        return self

    def __exit__(self, type, value, tb):
        # self.session.end_session()  <- mongodb mutex unlock
        pass

    def get_id(self) -> str:
        return self._id

    def pass_data(self, data):
        if data['members']:
            if len(data['members']) <= 4:
                self.team.set_members(list(set(data['members'])))
            else:
                raise ValueError("Team has more than 4 members")
        if data['eventID']:
            self.team.join_event(data['eventID'])
        if data['last_submission_timestamp']:
            self.team.set_last_submission_timestamp(data['last_submission_timestamp'])

    def create_team(self, owner, members: Optional[list]) -> bool:
        if not self.found:
            try:
                self.team.set_owner(owner)
                if members:
                    self.team.set_members(members)
                self.team.set_created_timestamp(str(datetime.utcnow()))
                self.commit()
                return True
            except Exception:
                return False
        else:
            return False

    def update_team(self, team) -> bool:
        query = {'name': self.team.name}
        self.pass_data(team)
        try:
            self.db.update_one(query, {'$set': self.team.covert_to_dict()})
            return True
        except Exception:
            return False

    def find_team(self):
        if self.team.name:
            team = self.db.find_one({'name': self.team.name})
            self._id = team['_id']
            return team
        return None
    
    def delete_team(self) -> bool:
        if self.found:
            if self.db.delete_one({'name': self.team.name}):
                return True
            else:
                return False
        return False

    def is_owner(self, email) -> bool:
        return email == self.team.owner

    def is_part_of_team(self, email) -> bool:
        return self.is_owner(email) or (email in self.team.members)

    def commit(self):
        query = {'name': self.team.name}
        data = self.team.covert_to_dict()
        self.db.update_one(query, {"$setOnInsert": data}, upsert=True)
