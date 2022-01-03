from typing import List, Optional
from bson.objectid import ObjectId

class MatchRequestModel:
    def __init__(self) -> None:
        self.teams = []
        self.event_id = None
        self.created_timestamp = None
    
    def __repr__(self) -> str:
        return f'{self.covert_to_dict()}'
    
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


class MatchResultModel:
    def __init__(self, teams: List[str], event_id: str, winner_id: Optional[str]=None) -> None:
        self.teams = teams
        self.event_id = event_id
        self.winner_id = winner_id
        self.created_timestamp = None

    def set_winner(self, winner_id: str) -> None:
        self.winner_id = winner_id

    def set_created_timestamp(self, time) -> None:
        self.created_timestamp = time

    def covert_to_dict(self) -> dict:
        return {'teams': self.teams,
                'event_id': self.event_id,
                'winner_id': self.winner_id,
                'created_timestamp': self.created_timestamp
                }
