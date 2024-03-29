from http import HTTPStatus

from flask import make_response, abort, jsonify
from flask_restful import Resource, reqparse
from bson.json_util import dumps

from server.Managers.Events.AdminEvents import EventsManager
from server.Managers.Auth.AdminManager import Admin_auth
from server.Managers.Leaderboard.LeaderboardManager import LeaderboardManager


class EventRoute(Resource):

    # flask parser for post request
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank"
    )
    parser.add_argument(
        "game", type=str, required=True, help="This field cannot be left blank"
    )
    parser.add_argument(
        "description", type=str, required=True, help="This field cannot be left blank"
    )
    parser.add_argument(
        "tutorial", type=str, required=True, help="This field cannot be left blank"
    )
    parser.add_argument(
        "starttime", type=str, required=True, help="This field cannot be left blank"
    )
    parser.add_argument(
        "endtime", type=str, required=True, help="This field cannot be left blank"
    )

    # flask parser for get request
    get_parser = reqparse.RequestParser()
    get_parser.add_argument(
        "name", type=str, required=False, help="If not provided, return all events"
    )

    @Admin_auth.login_required
    def post(self):
        data = EventRoute.parser.parse_args()
        with EventsManager(data["name"]) as eventmanager:
            result = eventmanager.create_event(
                data["game"],
                data["description"],
                data["tutorial"],
                data["starttime"],
                data["endtime"],
            )
        if result:
            with EventsManager(data["name"]) as eventmanager:
                event_dict = eventmanager.get_event_data()
            with LeaderboardManager() as leaderboardmanager:
                leaderboardmanager.create_event_leaderboard(event_dict)
            return make_response(
                jsonify({"message": "Event Created"}), HTTPStatus.CREATED
            )
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, "Could not create new event")

    # Get either a list of all events or details for a specific event if a "game" parameter is provided
    def get(self):
        data = EventRoute.get_parser.parse_args()
        if data["name"]:
            with EventsManager(data["name"]) as eventmanager:
                if eventmanager.found:
                    return make_response(dumps(eventmanager.event.covert_to_dict()), HTTPStatus.OK)
                abort(HTTPStatus.UNPROCESSABLE_ENTITY, "Could not find event")
        else:
            with EventsManager() as eventmanager:
                eventmanager.find_event()
                result = eventmanager.get_events()
                if result:
                    return make_response(dumps(result), HTTPStatus.OK)
                abort(HTTPStatus.UNPROCESSABLE_ENTITY, "Could not get events list")

    # Flask parser for delete request
    delete_parser = reqparse.RequestParser()
    delete_parser.add_argument(
        "name", type=str, required=True, help="This field cannot be left blank"
    )

    @Admin_auth.login_required
    def delete(self):
        data = EventRoute.delete_parser.parse_args()
        with EventsManager(data["name"]) as adminmanager:
            result = adminmanager.delete()
            if result:
                return make_response(
                    jsonify({"message": "Event Deleted"}), HTTPStatus.OK
                )
            abort(HTTPStatus.NOT_ACCEPTABLE, "Could not delete event")
