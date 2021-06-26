import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from .config import Configuration
from .Auth.register import RegisterRoute
from .Auth.verify import VerifyRoute
from .Database.mongodb import DatabaseCtrl

app = Flask(__name__)
CORS(app)
api = Api(app)


Mongo = DatabaseCtrl(Configuration.MONGODB_URI)


api.add_resource(RegisterRoute, '/register')
api.add_resource(VerifyRoute, '/verify/<code>')
# api.add_resource(VerifyRoute, '/verify/<string:code>')


if __name__ == '__main__':
    app.run()
