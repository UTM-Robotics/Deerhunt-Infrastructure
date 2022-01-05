from datetime import time
from http import HTTPStatus
from flask import make_response, abort, jsonify
from flask_restful import Resource, reqparse
from bson.json_util import dumps
from server.Managers.Events.AdminEvents import EventsManager

from server.Managers.Teams.TeamsManager import TeamsManager
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

    @User_auth.login_required
    def post(self):
        TeamsRoute.parser.add_argument(
            "event_id", type=str, required=True, help="This field cannot be left blank"
        )
        TeamsRoute.parser.add_argument("members", type=str, required=True)
        data = TeamsRoute.parser.parse_args()
        with TeamsManager(data["name"]) as teamsmanager:
            result = teamsmanager.create_team(data, User_auth.current_user())
            if result:
                return make_response(
                    jsonify({"message": "Team created successfuly."}),
                    HTTPStatus.CREATED,
                )
            abort(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                "Team with provided name already exists.",
            )

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
        if data["game"] != None and event_id == None:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, "No event found")
        with TeamsManager() as teamsmanager:
            result = teamsmanager.get_teams(User_auth.current_user())

            if result:
                if event_id:
                    for team in result:
                        if team["event_id"] == event_id:
                            return make_response(dumps(team), HTTPStatus.OK)
                    abort(HTTPStatus.UNPROCESSABLE_ENTITY, "No team for this event")
                return make_response(
                    dumps(result),
                    HTTPStatus.OK,
                )
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, "Could not fetch teams of user.")

    # @User_auth.login_required
    # def put(self):
    #     TeamsRoute.parser.add_argument('members', type=str, action="append")
    #     TeamsRoute.parser.add_argument('event_id', type=str)
    #     data = TeamsRoute.parser.parse_args()
    #     with TeamsManager(data['name']) as teamsmanager:
    #         if not teamsmanager.is_owner(User_auth.current_user()):
    #             return abort(HTTPStatus.UNAUTHORIZED, 'You are not the owner of this team.')
    #         result = teamsmanager.update_team(data)
    #         if result:
    #             return make_response(
    #                 jsonify(
    #                     {
    #                         'message': 'Successfully update the team'
    #                     }),
    #                 HTTPStatus.OK)
    #         return abort(HTTPStatus.BAD_REQUEST)

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
