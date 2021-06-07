from flask_restful import Api, Resource
from flask import make_response
from http import HTTPStatus



class RegisterRoute(Resource):
	def post(self):
		return make_response("Post works\n", HTTPStatus.OK)
