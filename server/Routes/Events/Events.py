from http import HTTPStatus

from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse
from bson.json_util import dumps

from server.Managers.Events.AdminEvents import EventsManager
from server.Managers.Auth.UserManager import User_auth
from server.Managers.Auth.AdminManager import Admin_auth


class EventRoute(Resource):

    # flask parser for post request
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('game', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('starttime', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('endtime', type=str, required=True, help='This field cannot be left blank')

    @Admin_auth.login_required
    def post(self):
        data = EventRoute.parser.parse_args()
        with EventsManager(data['name']) as admineventmanager:
            result = admineventmanager.create_event(data['game'],
                                                    data['starttime'],
                                                    data['endtime'])
            if result:
                return make_response(jsonify({'message': 'Event Created'}), HTTPStatus.CREATED)
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'Could not create new event')


    def get(self):
        with EventsManager() as admineventmanager:
            result = admineventmanager.get_events()
            if result:
                return make_response(dumps(result), HTTPStatus.OK)
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'Could not get events list')

    # Flask parser for delete request
    delete_parser = reqparse.RequestParser()
    delete_parser.add_argument('name', type=str, required=True, help='This field cannot be left blank')

    @Admin_auth.login_required
    def delete(self):
        data = EventRoute.delete_parser.parse_args()
        with EventsManager(data['name']) as adminmanager:
            result = adminmanager.delete()
            if result:
                return make_response(jsonify({'message': 'Event Deleted'}), HTTPStatus.OK)
            abort(HTTPStatus.NOT_ACCEPTABLE, 'Could not delete event')
            