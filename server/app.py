import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from pymongo import MongoClient

from .config import Configuration
from .Routes.register import RegisterRoute
# from .Routes.verify import VerifyRoute
# from .Routes.login import LoginRoute

app = Flask(__name__)
CORS(app)
api = Api(app)

Mongo = MongoClient(Configuration.MONGODB_URI)

api.add_resource(RegisterRoute, '/register')
# api.add_resource(VerifyRoute, '/verify/<code>')
# api.add_resource(LoginRoute, '/login')


if __name__ == '__main__':
    app.run()
