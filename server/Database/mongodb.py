from datetime import datetime
from passlib.hash import sha512_crypt
from pymongo import MongoClient

class DatabaseCtrl:
    def __init__(self, uri) -> None:
        cluster = MongoClient(uri)
        self.db = cluster['testing']

    @staticmethod
    def init_database(MongoURI: str):
        '''
        Returns single instance of DatabseCtrl for the entire app to use.
        The single instance is saved in Configuration class.
        '''
        return DatabaseCtrl(MongoURI)

    def find_user(self, email):
        '''
        Checks if account exists using email.
        '''
        return self.db.users.find_one({'email': email})

    def insert_user(self, email, passwd, newCode):
        '''
        Creates new user document in MongoDB.
        '''
        query = {'email': email}
        data = {'email': email,
                'password': sha512_crypt.encrypt(passwd),
                'code': newCode,
                'created_timestamp': str(datetime.now()),
                'verified': 'False'}
        return self.db.users.update_one(query, {"$setOnInsert": data}, upsert=True)

    def verify_code(self, code: str):
        '''
        Finds account with new code.
        '''
        query = {'code': code}
        result = self.db.users.find_one(query)
        if result is None:
            return False
        newvalues = {'$set': {'code': '',
                     'verified': 'True'}}
        self.db.users.update_one(query, newvalues)
        return True
