from http import HTTPStatus
from flask import make_response, request, abort, jsonify
from flask_restful import Resource

from server.Managers.UserManager import UserManager

class LoginRoute(Resource):
    def post(self):
        '''
        Handles post request for /login
        '''
        with UserManager(request.json['email']) as usermanager:
            result = usermanager.login(request.json['password'])
        if result:
            return make_response(jsonify({'token': result}), HTTPStatus.OK)
        return make_response("Username or Password is wrong", HTTPStatus.UNAUTHORIZED)
