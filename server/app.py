from .config import Configuration
from http import HTTPStatus
from flask import Flask, make_response
from flask_restful import Api, Resource
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)

class Auth(Resource):
	def post(self):
		return make_response("Post workss\n", HTTPStatus.OK)

api.add_resource(Auth, '/register')


if __name__ == '__main__':
    app.run()
