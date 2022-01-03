from datetime import time
from http import HTTPStatus
from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Teams.TeamsManager import TeamsManager
from server.Managers.Auth.UserManager import UserManager

from server.Managers.Auth.UserManager import User_auth


class UserTeamsRoute(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank"
    )

    @User_auth.login_required
    # Note: passing name parameter to route - /api/teams?name=<NAME>
    def get(self):
        user = None
        with UserManager(User_auth.current_user()) as usermanager:
            user = usermanager.user
        data = UserTeamsRoute.parser.parse_args()
        with TeamsManager(data["name"]) as teamsmanager:
            if not teamsmanager.is_part_of_team(user.email):
                return abort(HTTPStatus.UNAUTHORIZED)
            return teamsmanager.team.covert_to_dict()
