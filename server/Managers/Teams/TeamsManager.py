from datetime import datetime
from typing import List, Optional

from server.Database import Mongo
from server.Models.Teams.Teams import TeamsModel

from bson.objectid import ObjectId

class TeamsManager:
    def __init__(self, name=None) -> None:
        self.db = Mongo.teams
        self.team = TeamsModel(name)

    def __enter__(self):
        # self.session = Mongo.start_session()  <- mongodb mutex lock
        result = self.find_team()
        if result:
            self.team.set_id(result['_id'])
            self.team.set_owner(result['owner'])
            self.team.set_members(result['members'])
            self.team.set_event_id(result['event_id'])
            self.team.set_last_submission_timestamp(result['last_submission_timestamp'])
            self.team.set_last_challenge_timestamp(result['last_challenge_timestamp'])
            self.team.set_created_timestamp(result['created_timestamp'])
            self.found = True
        else:
            self.found = False
        return self

    def __exit__(self, type, value, tb):
        # self.session.end_session()  <- mongodb mutex unlock
        pass

    def create_team(self, event_id: str, owner: str) -> bool:
        if not self.found:
            self.team.set_owner(owner)
            self.team.set_members([owner])
            self.team.set_event_id(ObjectId(event_id))
            self.team.set_created_timestamp(datetime.now())
            self.commit()
            return True
        else:
            return False

    def get_teams(self, email: str):
        all_teams = list()
        for team in self.db.find({'members': email}):
            all_teams.append(team)
        return all_teams

    def find_team(self):
        if self.team.get_name():
            return self.db.find_one({'name': self.team.get_name()})
        return False

    def find_teams(self, ids):
        tmp = []
        for i in ids:
            tmp.append(self.db.find_one({"_id": i}))
        return tmp

    def find_team_by_id(self, id):
        return self.db.find_one({'_id': id})

    def commit(self):
        query = {'name': self.team.get_name()}
        data = self.team.covert_to_dict()
        if self.found:
            self.db.update_one(query, {'$set': data})
        else:
            self.db.update_one(query, {"$setOnInsert": data}, upsert=True)

    def commit_data(self, data):
        query = {'_id': data['_id']}
        self.db.update_one(query, {'$set': data})
