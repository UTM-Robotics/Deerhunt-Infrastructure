from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from pymongo import MongoClient

from .config import Configuration
from .Auth.register import RegisterRoute

app = Flask(__name__)
CORS(app)
api = Api(app)

# Mongo = MongoClient(Configuration.MONGODB_URI)


api.add_resource(RegisterRoute, '/register')


if __name__ == '__main__':
    app.run()
