from datetime import time
from http import HTTPStatus

import werkzeug
from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Teams.TeamsManager import TeamsManager
from server.Managers.Auth.UserManager import UserManager

from server.Managers.Auth.UserManager import User_auth


class SubmissionsRoute(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('file', type=werkzeug.datastructures.FileStorage,
                        location='files', required=True,
                        help='This field cannot be left blank')

    @User_auth.login_required
    def post(self):
        args = SubmissionsRoute.parser.parse_args()
        user_file = args['file']
