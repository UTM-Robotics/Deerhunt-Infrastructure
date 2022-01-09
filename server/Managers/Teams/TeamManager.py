from http import HTTPStatus
from typing import List

from flask import abort

from server.Database import Mongo
from server.Models.Teams.Teams import TeamsModel

import random


class TeamManager:
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
            self.team.set_last_submission_timestamp(
                result['last_submission_timestamp'])
            self.team.set_created_timestamp(result['created_timestamp'])
            self.found = True
        else:
            self.found = False
        return self

    def __exit__(self, type, value, tb):
        # self.session.end_session()  <- mongodb mutex unlock
        pass

    def find_team(self):
        if self.team.get_name():
            return self.db.find_one({'name': self.team.get_name()})
        return False

    def is_owner(self, email) -> bool:
        return email == self.team.get_owner()

    def is_part_of_team(self, email) -> bool:
        return self.is_owner(email) or (email in self.team.members)

    def update_members(self, members: List[str]):
        for member in members:
            user = Mongo.users.find_one({'email': member})
            if not user or not user['verified']:
                return abort(HTTPStatus.BAD_REQUEST,
                    f"{member} must invite registered and verified first")
        self.team.set_members(members)
        self.commit()
        return True

    def leave_team(self, user: str):
        if len(self.team.members) == 1:
          return self.db.delete_one({'name': self.team.name})
        if self.is_owner(user):
          new_owner = self.team.members[random.randint(0, len(self.team.members) - 1)]
          self.team.set_owner(new_owner)
        self.team.members.remove(user)
        self.commit()
        return True

    def get_teams(self, email: str):
        all_teams = list()
        for team in self.db.find({'members': email}):
            all_teams.append(team)
        return all_teams

    def commit(self):
        query = {'name': self.team.get_name()}
        data = self.team.covert_to_dict()
        if self.found:
            self.db.update_one(query, {'$set': data})
        else:
            self.db.update_one(query, {"$setOnInsert": data}, upsert=True)
