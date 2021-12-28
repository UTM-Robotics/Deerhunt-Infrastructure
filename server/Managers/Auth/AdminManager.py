import jwt

from flask_httpauth import HTTPTokenAuth

from datetime import datetime, timedelta

from server.Database import Mongo
from server.Models.User.AdminUser import AdminUserModel

from server.config import Configuration


'''
Creates decorator function for checking Admin account Bearer token.
Routes which have
                    @Admin_auth.login_required

Call the verify_token() function below.
'''
Admin_auth = HTTPTokenAuth(scheme='Bearer')
@Admin_auth.verify_token
def verify_token(token):
    admin = Mongo.admins.find_one({'jwt_token': token})
    if admin:
        try:
            jwt.decode(token, Configuration.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return False
        return admin['username']
    return False



class AdminManager:
    def __init__(self, username=None):
        self.db = Mongo.admins
        self.user = AdminUserModel(username)

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

    def login(self, password):
        if self.found and self.user.verify_password(password):
            now = datetime.utcnow()
            payload = {
            'iat': now,
            'exp': now + timedelta(minutes=60),
            'email': self.user.get_username()
            }
            newToken = jwt.encode(payload, Configuration.SECRET_KEY, algorithm='HS256')
            self.user.set_jwt_token(newToken)
            self.commit()
            return newToken
        else:
            return False

    def find_user(self):
        if self.user.get_username():
            return self.db.find_one({'username': self.user.get_username()})
        return None

    def commit(self):
        query = {'username': self.user.get_username()}
        data = self.user.covert_to_dict()
        if self.found:
            self.db.update_one(query, {'$set': data })
        else:
            self.db.update_one(query, {"$setOnInsert": data}, upsert=True)
