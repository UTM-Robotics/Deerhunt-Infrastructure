from http import HTTPStatus
from logging import fatal
from flask import make_response, request, abort
from flask_restful import Resource

from ..config import Configuration
from ..EmailBot.emailbot import EmailBot
from .codegenerator import CodeGenerator



def is_allowed(email: str) -> bool:
    '''
    Checks to see if provided email has allowed domain.
    '''
    for allowed_email in Configuration.MAIL_DOMAINS:
        if email.endswith(allowed_email):
            return True
    return False


class RegisterRoute(Resource):
    def post(self):
        '''
        Handles post request for /register        
        '''
        email = request.json['email']
        passwd = request.json['password']
        result = Configuration.Mongo.find_user(email)
        if result is not None:
            abort(409, 'User already exists')
        if not is_allowed(email):
            abort(409, 'Email domain not allowed')
        newCode = CodeGenerator.generate(8)
        Configuration.Mongo.insert_user(email, passwd, newCode)
        with EmailBot() as emailbot:
            emailbot.build_message_registration(newCode)
            emailbot.send(email)
        return make_response('Account partially created. Verification email sent\n', HTTPStatus.OK)
