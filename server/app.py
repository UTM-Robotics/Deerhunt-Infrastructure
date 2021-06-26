import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
# from pymongo import MongoClient

from .config import Configuration
from .Auth.register import RegisterRoute
from .Auth.verify import VerifyRoute


app = Flask(__name__)
CORS(app)
api = Api(app)
# Mongo = MongoClient(Configuration.MONGODB_URI).deerhunt_prod
# Mongo = MongoClient(Configuration.MONGODB_URI).deerhunt_db


api.add_resource(RegisterRoute, '/register')
api.add_resource(VerifyRoute, '/verify/<code>')
# api.add_resource(VerifyRoute, '/verify/<string:code>')


if __name__ == '__main__':
    app.run()
