from pymongo import MongoClient
from datetime import datetime
from passlib.hash import sha512_crypt


from server.config import Configuration


if Configuration.ENV == 'development':
    Mongo = MongoClient(Configuration.MONGODB_URI)['testing']
    print('\n Using Database testing')
elif Configuration.ENV == 'production':
    Mongo = MongoClient(Configuration.MONGODB_URI)['production']
    print('\n Using Database production')


def create_default_admin() -> None:
    '''
    Checks if default admin account exists in DB.
    Creates it if it doesn't exist.
    '''
    if not Mongo.admins.find_one({'username': Configuration.ADMIN_USERNAME}):
        query = {'username': Configuration.ADMIN_USERNAME}
        data = {'username': Configuration.ADMIN_USERNAME,
                'password': sha512_crypt.hash(Configuration.ADMIN_PASSWORD),
                'created_timestamp': str(datetime.utcnow()),
                'jwt_token': ''
                }
        Mongo.admins.update_one(query, 
                                {"$setOnInsert": data},
                                upsert=True)
        print(' Created default Admin account\n')
    else:
        print(' Admin account already exists \n')

create_default_admin()
