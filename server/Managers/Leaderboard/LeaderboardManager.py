
from os import environ
from server.Database import Mongo
from server.Models.Leaderboard.Leaderboard import LeaderboardModel



class LeaderboardManager:
    def __init__(self):
        self.db = Mongo.leaderboards
        self.leaderboard = LeaderboardModel()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    def create_event_leaderboard(self, event_dict: dict):
        self.leaderboard.set_name(event_dict['name'])
        self.leaderboard.set_event_id(event_dict['_id'])
        query = {'name': self.leaderboard.get_name()}
        data = self.leaderboard.covert_to_dict()
        self.db.update_one(query, {"$setOnInsert": data}, upsert=True)
