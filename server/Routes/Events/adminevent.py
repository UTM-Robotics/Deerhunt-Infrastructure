from http import HTTPStatus
from flask import make_response, request, abort, jsonify
from flask_restful import Resource

from server.Managers.Events.AdminEvents import AdminEventsManager

from server.Managers.Auth.UserManager import auth


class AdminEventRoute(Resource):

    @auth.login_required
    def post(self):
        with AdminEventsManager(request.json['title']) as admineventmanager:
            pass
