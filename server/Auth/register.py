from http import HTTPStatus
from flask import make_response, request, abort
from flask_restful import Resource

from ..EmailBot.emailbot import EmailBot
from .codegenerator import CodeGenerator
from ..app import Mongo


class RegisterRoute(Resource):
    def post(self):
        email = request.json['email']
        passwd = request.json['passwd']
        result = Mongo.find_user(email)
        if result is not None:
            abort(409, 'User already exists')
        newCode = CodeGenerator.generate(8)
        Mongo.insert_user(email, passwd, newCode)
        with EmailBot() as emailbot:
            emailbot.build_message_registration(newCode)
            emailbot.send(email)
        return make_response('Email Sent\n', HTTPStatus.OK)
