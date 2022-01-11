from http import HTTPStatus

from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Events.AdminEvents import EventsManager
from server.Managers.Teams.TeamsManager import TeamsManager
from server.Managers.Auth.UserManager import UserManager, User_auth
from server.Models.User import AdminUser, GeneralUser


class UserTeamRoute(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=False, help="This field cannot be left blank"
    )

    @User_auth.login_required
    def post(self):
        data = UserTeamRoute.parser.parse_args()
        with UserManager(User_auth.current_user()) as usermanager:
            if usermanager.found:
                with TeamsManager() as teamsmanager:
                    result = teamsmanager.get_teams(usermanager.user.get_email())
                    if result:
                        with EventsManager(data['name']) as eventsmanager:
                            if not eventsmanager.found:
                                return make_response(jsonify({"message": "No event found"}), HTTPStatus.NOT_FOUND)
                            event_team = None

                            for team in result:
                                if team['event_id'] == eventsmanager.event.get_id():
                                    event_team = team
                                    break
                            if event_team is not None:
                                event_team['_id'] = str(event_team['_id'])
                                event_team['event_id'] = str(event_team['event_id'])
                                return make_response(jsonify(event_team), HTTPStatus.OK)
                    return make_response(jsonify({"message": "No teams found"}), HTTPStatus.NOT_FOUND)
            return make_response(jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND)