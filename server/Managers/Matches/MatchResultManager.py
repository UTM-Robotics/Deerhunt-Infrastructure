from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from server.Database import Mongo
from server.Models.Matches.Matches import MatchResultModel


class MatchResultManager:
    def __init__(self) -> None:
        self.db = Mongo.matches
        self.match = MatchResultModel()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    def get_id(self) -> str:
        return self._id

    def pass_data(self, data) -> None:
        self.match.set_event(data['event_id'])
        self.match.set_winner(data['winner_id'])
        self.match.set_loser(data['loser_id'])

    def create_match(self, data) -> bool:
        try:
            self._id = data['match_id']
            self.pass_data(data)
            self.match.set_created_timestamp(str(datetime.utcnow()))
            self.commit()
            return True
        except Exception:
            return False

    def find_match(self, id):
        match = self.db.find_one({'_id': ObjectId(id)})
        if match:
            self._id = id
            self.pass_data(match)
            self.match.set_created_timestamp(match['created_timestamp'])
            return self.match.covert_to_dict()
        return None

    def commit(self) -> None:
        self.db.insert_one({'_id': ObjectId(self.get_id()), 'event_id': self.match.event_id, 'winner_id': self.match.winner_id, 'loser_id': self.match.loser_id, 'created_timestamp': self.match.created_timestamp})
