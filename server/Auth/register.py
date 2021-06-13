from flask_restful import Api, Resource
from flask import make_response, request
from http import HTTPStatus
from ..EmailBot.emailbot import EmailBot


class RegisterRoute(Resource):
    def post(self):
        print(request.json)
        username = request.json['username']
        # result = database.users.find_one({'username': u})  <--- Need DB setup
        with EmailBot(purpose='registration') as email:
            email.send(username)
        return make_response("Post works\n", HTTPStatus.OK)
