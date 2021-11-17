from http import HTTPStatus

from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse
	
from server.Managers.Auth.UserManager import UserManager

class RegisterRoute(Resource):

    # flask parser
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')

    # Handles post request for user registration.
    def post(self):
        data = RegisterRoute.parser.parse_args()
        with UserManager(data['email']) as usermanager:
            result = usermanager.register(data['password'])
        if result:
            return make_response(jsonify({'message': 'Account partially created. Verification email sent\n'}), 
                                HTTPStatus.OK)
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'User already exists')
