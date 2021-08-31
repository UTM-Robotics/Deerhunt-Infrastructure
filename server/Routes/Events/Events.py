from http import HTTPStatus
from flask import make_response, request, abort, jsonify
from flask_restful import Resource

from server.Managers.Events.AdminEvents import EventsManager

from server.Managers.Auth.UserManager import User_auth
from server.Managers.Auth.AdminManager import Admin_auth


class EventRoute(Resource):

    @Admin_auth.login_required
    def post(self):
        with EventsManager(request.json['name']) as admineventmanager:
            result = admineventmanager.create_event(request.json['game'],
                                                    request.json['starttime'],
                                                    request.json['endtime'])
            if result:
                return make_response(jsonify({'message': 'Event Created'}), HTTPStatus.CREATED)
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'Could not create new event')


    def get(self):
        with EventsManager() as admineventmanager:
            result = admineventmanager.get_events()
            if result:
                return make_response(jsonify(result), HTTPStatus.OK)
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'Could not get events list')