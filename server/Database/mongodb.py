from datetime import datetime
from passlib.hash import sha512_crypt
from pymongo import MongoClient

class DatabaseCtrl:
    def __init__(self, uri) -> None:
        cluster = MongoClient(uri)
        self.db = cluster['testing']

    def find_user(self, email):
        return self.db.users.find_one({'email': email})

    def insert_user(self, email, passwd, newCode):
        query = {'email': email}
        data = {'email': email,
                'password': sha512_crypt.encrypt(passwd),
                'code': newCode,
                'created_timestamp': str(datetime.now()),
                'verified': 'False'}
        # self.db.users.update_one()