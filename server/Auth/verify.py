from flask_restful import Api, Resource
from flask import make_response, request
from http import HTTPStatus


class VerifyRoute(Resource):
    def post(self):
        codeName = request.json['code']
        # result = database.users.find_one({'username': u})  <--- Need DB setup

