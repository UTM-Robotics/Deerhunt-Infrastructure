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
            self.team.set_last_submission_timestamp(['last_submission_timestamp'])
            self.team.set_created_timestamp(result['created_timestamp'])
            self.found = True
        else:
            self.found = False
        return self

    def __exit__(self, type, value, tb):
        # self.session.end_session()  <- mongodb mutex unlock
        pass

    def create_team(self, teamdata: dict, owner: str) -> bool:
        if not self.found:
            self.team.set_owner(owner)
            self.team.set_members([owner] + (teamdata['members'].split()))
            self.team.set_event_id(ObjectId(teamdata['event_id']))
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

    def update_team(self, teamdata) -> bool:
        self.team.set_event_id(ObjectId(teamdata['event_id']))
        self.team.set_members((teamdata['members'].split()))
        query = {'name': self.team.name}
        try:
            self.db.update_one(query, {'$set': self.team.covert_to_dict()})
            return True
        except Exception:
            return False

    def find_team(self):
        if self.team.get_name():
            return self.db.find_one({'name': self.team.get_name()})
        return False

    def find_teams(self, ids):
        tmp = []
        for i in ids:
            tmp.append(self.db.find_one({"_id": i}))
        return tmp
    
    def commit(self):
        query = {'name': self.team.get_name()}
        data = self.team.covert_to_dict()
        if self.found:
            self.db.update_one(query, {'$set': data})
        else:
            self.db.update_one(query, {"$setOnInsert": data}, upsert=True)


    # def delete_team(self) -> bool:
    #     if self.found:
    #         if self.db.delete_one({'name': self.team.name}):
    #             return True
    #         else:
    #             return False
    #     return False

    # def is_owner(self, email) -> bool:
    #     return email == self.team.get_owner()

    # def is_part_of_team(self, email) -> bool:
    #     return self.is_owner(email) or (email in self.team.members)

    # def add_members(self, members: List[str]) -> None:
    #     for member in members:
    #         user = Mongo.users.find_one({'email': member})
    #         if not user or not user['verified']:
    #             raise ValueError(
    #                 "Must invite registered and verified member(s)")
    #         elif self.is_part_of_team(member):
    #             raise ValueError("Already added such members")
    #         else:
    #             self.team.set_members([member])


    # def find_team_by_id(self, team_id):
    #     team = self.db.find_one({'_id': team_id})
    #     if team:
    #         self._id = team['_id']
    #         return team
    #     return None

    # def find_by_event_username(self, event_id, username):
    #     team = self.db.find_one({'event_id': event_id, 'members': username})
    #     if team:
    #         self._id = team['_id']
    #         self.team.set_owner(team['owner'])
    #         self.team.set_created_timestamp(team['created_timestamp'])
    #         self.pass_data(team)
    #         self.found = True
    #     return None
