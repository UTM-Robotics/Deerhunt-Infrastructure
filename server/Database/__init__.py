from pymongo import MongoClient
from server.config import Configuration
Mongo = MongoClient(Configuration.MONGODB_URI)['testing']