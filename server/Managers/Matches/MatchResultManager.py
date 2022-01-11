from datetime import datetime

from bson import ObjectId
from dotenv.main import set_key

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
        self.match.set_event(data["event_id"])
        self.match.set_winner(data["winner_id"])
        self.match.set_loser(data["loser_id"])

    def create_match(self, data) -> bool:
        try:
            self.pass_data(data)
            self.match.set_created_timestamp(str(datetime.utcnow()))
            self.commit()
            return True
        except Exception:
            return False

    def find_match(self, id):
        match = self.db.find_one({"_id": ObjectId(id)})
        if match:
            self._id = id
            self.pass_data(match)
            self.match.set_created_timestamp(match["created_timestamp"])
            return self.match.covert_to_dict()
        return None

    def find_all_matches(self, event_id):
        return self.db.find({"event_id": ObjectId(event_id)})

    def commit(self) -> None:
        res = self.db.insert_one(
            {
                "event_id": self.match.event_id,
                "winner_id": self.match.winner_id,
                "loser_id": self.match.loser_id,
                "created_timestamp": self.match.created_timestamp,
            }
        )
        self._id = res.inserted_id
