from pymongo import MongoClient
from server.config import Configuration
Mongo = MongoClient(Configuration.MONGODB_URI)['testing']

def create_default_admin():
    default = Mongo.admins.find_one({'username': Configuration.ADMIN_USERNAME})
    if not default:
        data = {'username': Configuration.ADMIN_USERNAME,
                'password'}
        Mongo.admins.update_one(
                    {'username': Configuration.ADMIN_USERNAME}, 
                    {"$setOnInsert": data}, upsert=True)
    return None


# query = {'email': self.user.get_email()}
# data = self.user.covert_to_dict()
# if self.found:
#     self.db.update_one(query, {'$set': data })
# else:
#     self.db.update_one(query, {"$setOnInsert": data}, upsert=True)
