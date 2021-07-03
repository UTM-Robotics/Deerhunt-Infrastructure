from http import HTTPStatus
from flask import make_response, request, abort
from flask_restful import Resource

from server.Managers.UserManager import UserManager

class RegisterRoute(Resource):
    def post(self):
        '''
        Handles post request for /register        
        '''
        with UserManager(request.json['email']) as usermanager:
            result = usermanager.register(request.json['password'])
        if result:
            return make_response('Account partially created. Verification email sent\n', HTTPStatus.OK)
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'User already exists')
