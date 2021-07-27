import random, string, jwt

from datetime import datetime, timedelta

from server.Database import Mongo
from server.Models.AdminModel import AdminModel
from server.Managers.EmailBot.EmailBot import EmailBot

from server.config import Configuration




class AdminManager:
    def __init__(self, username=None):
        self.db = Mongo.admins
        self.user = AdminModel(username)

    def __enter__(self):
        result = self.find_user()
        if result:
            self.user.set_username(result['username'])
            self.user.set_password(result['password'])
            self.user.set_created_timestamp(result['created_timestamp'])
            self.user.set_jwt_token(result['jwt_token'])
            self.found = True
        else:
            self.found = False
        return self

    def __exit__(self, type, value, tb):
        pass

    def find_user(self):
        if self.user.get_username():
            return self.db.find_one({'email': self.user.get_email()})
        return None
