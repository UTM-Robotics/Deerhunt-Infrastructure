from http import HTTPStatus
from flask import make_response, request, abort
from flask_restful import Resource
from passlib.hash import sha512_crypt


from ..config import Configuration
from ..EmailBot.emailbot import EmailBot
from .codegenerator import CodeGenerator


class LoginRoute(Resource):
    def post(self):
        '''
        Handles post request for /register   
        '''
        email = request.json['email']
        password = request.json['password']
        result = Configuration.Mongo.login(email, password)
        if not result:
            abort(HTTPStatus.NOT_FOUND, 'User does not exist or password is wrong')
        return make_response('Login successful.\n', HTTPStatus.OK)
