from datetime import time
from http import HTTPStatus
from flask import make_response, abort, jsonify
from flask_restful import Resource, reqparse
from bson.json_util import dumps

from server.Managers.Teams.TeamManager import TeamManager
from server.Managers.Events.AdminEvents import EventsManager

from server.Managers.Teams.TeamsManager import TeamsManager
from server.Managers.Leaderboard.LeaderboardManager import LeaderboardManager
from server.Managers.Events.AdminEvents import EventsManager
from server.Managers.Auth.UserManager import User_auth


class AddTeam(Resource):
    put_parser = reqparse.RequestParser()
    put_parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank"
    )
    put_parser.add_argument(
        "email", type=str, required=True, help="This field cannot be left blank"
    )

    @User_auth.login_required
    def post(self):
        data = AddTeam.put_parser.parse_args()
        with TeamManager(data['name']) as teamsmanager:
            if not teamsmanager.is_owner(User_auth.current_user()):
                return make_response(jsonify({"message": "You are not the owner of this team."}),
                                     HTTPStatus.UNAUTHORIZED)
            teams = teamsmanager.get_teams(data['email'])
            if teams:
                return make_response(jsonify({"message": "User is already on a team."}),
                                     HTTPStatus.UNPROCESSABLE_ENTITY)
            if len(teamsmanager.team.get_members()) >= 4:
                return make_response(jsonify({"message": "Team is full."}), HTTPStatus.UNPROCESSABLE_ENTITY)
            result = teamsmanager.update_members(teamsmanager.team.get_members() + [data['email']])
            if result is True:
                team = teamsmanager.team.covert_to_dict()
                team['_id'] = str(team['_id'])
                team['event_id'] = str(team['event_id'])
                return make_response(jsonify(team), HTTPStatus.OK)
            make_response(jsonify({"message": "Something went wrong."}), HTTPStatus.INTERNAL_SERVER_ERROR)
