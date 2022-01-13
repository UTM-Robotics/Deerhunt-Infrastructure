from typing import List
from bson.objectid import ObjectId

class MatchResultModel:
    def __init__(self) -> None:
        self.event_id = None
        self.winner_id = None
        self.loser_id = None
        self.created_timestamp = None
        self.default = None

    def set_event(self, event_id: str) -> None:
        self.event_id = ObjectId(event_id)
    
    def set_winner(self, winner_id: str) -> None:
        self.winner_id = ObjectId(winner_id)
    
    def set_loser(self, loser_id: str) -> None:
        self.loser_id = ObjectId(loser_id)

    def set_created_timestamp(self, time) -> None:
        self.created_timestamp = time
    def set_default(self, default_message)-> None:
        self.default = default_message
    def covert_to_dict(self) -> dict:
        if "default" != None:
            return {'event_id': str(self.event_id),
                    'winner_id': str(self.winner_id),
                    'loser_id': str(self.loser_id),
                    'created_timestamp': self.created_timestamp,
                    'default': self.default
                    }
        return {'event_id': str(self.event_id),
                'winner_id': str(self.winner_id),
                'loser_id': str(self.loser_id),
                'created_timestamp': self.created_timestamp
                }
