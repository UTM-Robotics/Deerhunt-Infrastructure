import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from .Auth.register import RegisterRoute
from .Auth.verify import VerifyRoute

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(RegisterRoute, '/register')
api.add_resource(VerifyRoute, '/verify/<code>')


if __name__ == '__main__':
    app.run()
