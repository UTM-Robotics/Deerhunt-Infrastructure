from http import HTTPStatus

from flask import make_response, request, abort
from flask_restful import Resource, reqparse
from bson.json_util import dumps

from server.Managers.Leaderboard.LeaderboardManager import LeaderboardManager
from server.Managers.Teams.TeamsManager import TeamsManager
from server.Managers.Auth.UserManager import User_auth


class LeaderboardRoute(Resource):

    # flask parser for post request
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank"
    )

    @User_auth.login_required
    def get(self):
        data = LeaderboardRoute.parser.parse_args()
        with LeaderboardManager() as leaderboardmanager:
            all_team_ids = leaderboardmanager.get_leaderboard(data["name"])
            if all_team_ids:
                with TeamsManager() as teamsmanager:
                    teams_leaderboard = teamsmanager.find_teams(
                        all_team_ids["team_ids"]
                    )
                    if teams_leaderboard:
                        return make_response(dumps(teams_leaderboard), HTTPStatus.OK)
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, "Could not fetch leaderboard for event")
