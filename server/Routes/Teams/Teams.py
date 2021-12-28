from http import HTTPStatus
from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Teams.TeamsManager import TeamsManager
from server.Managers.Auth.UserManager import UserManager

from server.Managers.Auth.UserManager import User_auth


class TeamsRoute(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help='This field cannot be left blank')

    @User_auth.login_required
    def post(self):
        user = None
        with UserManager(User_auth.current_user()) as usermanager:
            user = usermanager.user
        data = TeamsRoute.parser.parse_args()
        with TeamsManager(data['name']) as teamsmanager:
            if teamsmanager.find_team():
                return abort(HTTPStatus.BAD_REQUEST)
            if teamsmanager.createTeam(user.email):
                return make_response(jsonify({'message': 'Successfully created a team'}), HTTPStatus.OK)
