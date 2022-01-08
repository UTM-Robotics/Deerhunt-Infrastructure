from datetime import time
from http import HTTPStatus
from flask import make_response, abort, jsonify
from flask_restful import Resource, reqparse
from bson.json_util import dumps

from Managers.Teams.TeamManager import TeamManager
from server.Managers.Events.AdminEvents import EventsManager

from server.Managers.Teams.TeamsManager import TeamsManager
from server.Managers.Leaderboard.LeaderboardManager import LeaderboardManager
from server.Managers.Events.AdminEvents import EventsManager
from server.Managers.Auth.UserManager import User_auth


class TeamsRoute(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank"
    )

    # Flask parser for get request
    get_parser = reqparse.RequestParser()
    get_parser.add_argument(
        "game",
        type=str,
        required=False,
        help="If not provided, return all teams that the user is on",
    )

    put_parser = reqparse.RequestParser()
    put_parser.add_argument(
        "name", type=str, required=False, help="This field cannot be left blank"
    )
    put_parser.add_argument(
        "email", type=str, required=True, help="This field cannot be left blank"
    )

    @User_auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "name", type=str, required=True, help="This field cannot be left blank"
        )
        parser.add_argument(
            "event_name",
            type=str,
            required=True,
            help="This field cannot be left blank",
        )
        data = parser.parse_args()
        with EventsManager(data["event_name"]) as eventmanager:
            pass
            # eventdata = eventmanager.find_event()
            # data["event_id"] = eventdata["_id"]
            with TeamsManager(data["name"]) as teamsmanager:
                teams = teamsmanager.get_teams(User_auth.current_user())
                for team in teams:
                    if team["event_id"] == eventmanager.event.get_id():
                        return make_response(jsonify({"message": "You are already on a team for this event."}),
                                             HTTPStatus.UNPROCESSABLE_ENTITY)
                result = teamsmanager.create_team(str(eventmanager.event.get_id()), User_auth.current_user())
                if result:
                    with TeamsManager(data["name"]) as teamsmanager:
                        team_data = teamsmanager.find_team()
                        team_data["_id"] = str(team_data["_id"])
                        team_data["event_id"] = str(team_data["event_id"])
                        print(team_data)
                        with LeaderboardManager() as leaderboardmanager:
                            leaderboardmanager.add_to_leaderboard(team_data)
                        return make_response(
                            jsonify({"message": "Team created successfully.", "team": team_data}),
                            HTTPStatus.CREATED,
                        )
            make_response(jsonify({"message": "Team with that name already exists."}), HTTPStatus.UNPROCESSABLE_ENTITY)

    @User_auth.login_required
    def get(self):
        event_id = None
        with EventsManager() as eventmanager:
            result = eventmanager.get_events()
            if result:
                data = TeamsRoute.get_parser.parse_args()
                if data["game"]:
                    for event in result:
                        if event["game"] == data["game"]:
                            event_id = str(event["_id"])
        if data["game"] is not None and event_id is None:
            return make_response(jsonify({"message": "No event with that name exists."}), HTTPStatus.NOT_FOUND)
        with TeamsManager() as teamsmanager:
            result = teamsmanager.get_teams(User_auth.current_user())

            if result:
                if event_id:
                    for team in result:
                        if team["event_id"] == event_id:
                            return make_response(dumps(team), HTTPStatus.OK)
                    return make_response(jsonify({"message": "No teams for this event."}), HTTPStatus.NOT_FOUND)
                return make_response(
                    dumps(result),
                    HTTPStatus.OK,
                )
            return make_response(jsonify({"message": "Could not fetch teams of user."}), HTTPStatus.UNPROCESSABLE_ENTITY)

    # @User_auth.login_required
    # def delete(self):
    #     user = None
    #     with UserManager(User_auth.current_user()) as usermanager:
    #         user = usermanager.user
    #     data = TeamsRoute.parser.parse_args()
    #     with TeamsManager(data['name']) as teamsmanager:
    #         if not teamsmanager.is_owner(user.email):
    #             return abort(HTTPStatus.UNAUTHORIZED)
    #         if teamsmanager.delete_team():
    #             return make_response(jsonify({'message': 'Team deleted'}), HTTPStatus.OK)
    #         return abort(HTTPStatus.BAD_REQUEST)
