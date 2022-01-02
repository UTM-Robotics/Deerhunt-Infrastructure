import uuid
from datetime import datetime
from typing import List, Optional

from server.Database import Mongo
from server.Models.Teams.Teams import TeamsModel

from server.config import Configuration


class TeamsManager:
    def __init__(self, name):
        self.db = Mongo.teams
        self.team = TeamsModel(name)

    def __init__(self):
        self.db = Mongo.teams
        self.team = TeamsModel()

    def __enter__(self):
        # self.session = Mongo.start_session()  <- mongodb mutex lock
        result = self.find_team()
        if result:
            self.team.set_owner(result['owner'])
            self.team.set_created_timestamp(result['created_timestamp'])
            self.team.set_uuid(result['uuid'])
            self.pass_data(result)
            self.found = True
        else:
            self.found = False
        return self

    def __exit__(self, type, value, tb):
        # self.session.end_session()  <- mongodb mutex unlock
        pass

    def get_id(self) -> str:
        return self.team.uuid

    def get_by_id(self, team_id: str) -> bool:
        team = self.db.find_one({'uuid': team_id})
        if team:
            self.team.name = team['name']
            self.team.set_owner(team['owner'])
            self.team.set_created_timestamp(team['created_timestamp'])
            self.team.set_uuid(team['uuid'])
            self.pass_data(team)
            self.found = True

        return False

    def pass_data(self, data) -> None:
        if data['members']:
            self.add_members(list(set(data['members'])))
        if data['event_id']:
            self.team.join_event(data['event_id'])
        if data['last_submission_timestamp']:
            self.team.set_last_submission_timestamp(
                data['last_submission_timestamp'])
        if data['submissions']:
            self.team.set_submissions(data['submissions'])

    def create_team(self, owner: str, data) -> bool:
        if not self.found:
            try:
                self.team.join_event(data['event_id'])
                if not self.does_participate_event(owner, self.team.event_id):
                    self.team.set_owner(owner)
                else:
                    raise ValueError("You already have team in this event")
                if data['members']:
                    self.add_members(list(set(data['members'])))
                self.team.set_created_timestamp(str(datetime.utcnow()))
                self.team.uuid = str(uuid.uuid4())
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
        team = self.db.find_one({'name': self.team.name})
        if team:
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

    def does_own_team(self, email, event) -> bool:
        if self.db.find_one({"owner": email, "event_id": event}):
            return True
        return False

    def does_have_team(self, email, event) -> bool:
        if self.db.find_one({"members": email, "event_id": event}):
            return True
        return False

    def does_participate_event(self, email, event) -> bool:
        return self.does_own_team(email, event) or self.does_have_team(email, event)

    def add_members(self, members: List[str]) -> None:
        for member in members:
            user = Mongo.users.find_one({'email': member})
            if not user or not user['verified']:
                raise ValueError(f'Member {member} must be registered and verified first')
            elif self.is_part_of_team(member):
                raise ValueError(f'Member {member} is already in your team')
            elif self.does_participate_event(member, self.team.event_id):
                raise ValueError(f'Member {member} already has a team')
            else:
                self.team.set_members([member])

    def commit(self):
        query = {'name': self.team.name}
        data = self.team.covert_to_dict()
        self.db.update_one(query, {"$setOnInsert": data}, upsert=True)
