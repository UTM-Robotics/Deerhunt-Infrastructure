from http import HTTPStatus

from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse
	
from server.Managers.Auth.UserManager import UserManager

class ForgotPasswordRoute(Resource):

    # flask parser
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help='This field cannot be left blank')

    # Handles post request for user registration.
    def post(self):
        data = ForgotPasswordRoute.parser.parse_args()
        # send email to email for /api/user/changepassword_f/<code>