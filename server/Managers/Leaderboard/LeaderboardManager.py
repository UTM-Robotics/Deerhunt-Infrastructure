from os import environ

from pymongo.message import _Query
from server.Database import Mongo
from bson.objectid import ObjectId
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
        self.leaderboard.set_name(event_dict["name"])
        self.leaderboard.set_event_id(event_dict["_id"])
        query = {"name": self.leaderboard.get_name()}
        data = self.leaderboard.covert_to_dict()
        self.db.update_one(query, {"$setOnInsert": data}, upsert=True)

    def add_to_leaderboard(self, team_data: dict):
        leaderboard = self.db.find_one({"event_id": ObjectId(team_data["event_id"])})
        leaderboard["team_ids"].append(ObjectId(team_data["_id"]))
        print(leaderboard)
        query = {"event_id": ObjectId(team_data["event_id"])}
        self.db.update_one(query, {"$set": leaderboard})

    def get_leaderboard(self, name: str):
        leaderboard = self.db.find_one({"name": name})
        return leaderboard

    def update_leaderboard(self, leaderboard_data: dict, data: dict):
        query = {"_id": leaderboard_data["_id"]}
        winner = ObjectId(data["winner_id"])
        loser = ObjectId(data["loser_id"])
        teams = leaderboard_data["team_ids"]
        winner_index = teams.index(winner)
        loser_index = teams.index(loser)
        if winner_index > loser_index:
            teams[winner_index], teams[loser_index] = (
                teams[loser_index],
                teams[winner_index],
            )
        self.db.update_one(query, {"$set": {"team_ids": teams}})
