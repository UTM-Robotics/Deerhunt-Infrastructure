from datetime import time
from http import HTTPStatus
from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Teams.TeamsManager import TeamsManager
from server.Managers.Auth.UserManager import UserManager

from server.Managers.Auth.UserManager import User_auth


class TeamsRoute(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cannot be left blank')

    @User_auth.login_required
    def post(self):
        user = None
        with UserManager(User_auth.current_user()) as usermanager:
            user = usermanager.user
        TeamsRoute.parser.add_argument('event_id', type=str, required=True,
                            help='This field cannot be left blank')
        TeamsRoute.parser.add_argument('members', type=str, action="append")
        data = TeamsRoute.parser.parse_args()
        with TeamsManager(data['name']) as teamsmanager:
            if teamsmanager.find_team():
                return abort(HTTPStatus.BAD_REQUEST)
            if teamsmanager.create_team(user.email):
                return make_response(jsonify({'message': 'Successfully created a team'}), HTTPStatus.OK)
            else:
                raise SystemError("Error occurs when create a team")

    @User_auth.login_required
    # Note: passing name parameter to route - /api/teams?name=<NAME>
    def get(self):
        user = None
        with UserManager(User_auth.current_user()) as usermanager:
            user = usermanager.user
        data = TeamsRoute.parser.parse_args()
        with TeamsManager(data['name']) as teamsmanager:
            if not teamsmanager.is_part_of_team(user.email):
                return abort(HTTPStatus.UNAUTHORIZED)
            return teamsmanager.team.covert_to_dict()

    @User_auth.login_required
    def put(self):
        user = None
        with UserManager(User_auth.current_user()) as usermanager:
            user = usermanager.user
        TeamsRoute.parser.add_argument('members', type=str, action="append")
        TeamsRoute.parser.add_argument('event_id', type=str)
        TeamsRoute.parser.add_argument('last_submission_timestamp', type=time)
        data = TeamsRoute.parser.parse_args()
        with TeamsManager(data['name']) as teamsmanager:
            if not teamsmanager.is_owner(user.email):
                return abort(HTTPStatus.UNAUTHORIZED)
            if teamsmanager.update_team(data):
                return make_response(jsonify({'message': 'Successfully update the team'}), HTTPStatus.OK)
            return abort(HTTPStatus.BAD_REQUEST)

    @User_auth.login_required
    def delete(self):
        user = None
        with UserManager(User_auth.current_user()) as usermanager:
            user = usermanager.user
        data = TeamsRoute.parser.parse_args()
        with TeamsManager(data['name']) as teamsmanager:
            if not teamsmanager.is_owner(user.email):
                return abort(HTTPStatus.UNAUTHORIZED)
            if teamsmanager.delete_team():
                return make_response(jsonify({'message': 'Team deleted'}), HTTPStatus.OK)
            return abort(HTTPStatus.BAD_REQUEST)
