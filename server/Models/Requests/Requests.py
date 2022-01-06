from typing import List, Optional
from bson.objectid import ObjectId


class MatchRequestModel:
    def __init__(self) -> None:
        self.teams = []
        self.event_id = None
        self.created_timestamp = None

    def set_event(self, event_id: str) -> None:
        self.event_id = ObjectId(event_id)

    def set_teams(self, teams: List[str]) -> None:
        for team in teams:
            self.teams.append(ObjectId(team))

    def set_created_timestamp(self, time) -> None:
        self.created_timestamp = time

    def stringify_team_ids(self):
        lst = []
        for team in self.teams:
            lst.append(str(team))
        return lst

    def covert_to_dict(self) -> dict:
        return {'teams': self.stringify_team_ids(),
                'event_id': str(self.event_id),
                'created_timestamp': self.created_timestamp
                }
