from flask_restful import Api, Resource
from flask import make_response, request
from http import HTTPStatus

from ..EmailBot.emailbot import EmailBot
from .codegenerator import CodeGenerator


class RegisterRoute(Resource):
    def post(self):
        email = request.json['email']
        # result = database.users.find_one({'username': u})  <--- Need DB setup
        with EmailBot() as emailbot:
            emailbot.build_message_registration(CodeGenerator.generate(8))
            emailbot.send(email)
        return make_response('Email Sent\n', HTTPStatus.OK)
