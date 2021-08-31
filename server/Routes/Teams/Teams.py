from http import HTTPStatus
from flask import make_response, request, abort, jsonify
from flask_restful import Resource

from server.Managers.Teams.TeamsManager import TeamsManager

from server.Managers.Auth.UserManager import User_auth


class TeamsRoute(Resource):

    @User_auth.login_required
    def post(self):
        email = auth.current_user()
        with UserManager(auth.current_user()) as usermanager:
            pass # check that user isn't part of team
        with TeamsManager(request.json['name']) as teamsmanager:
            pass # check that new team 'name' doesn't exist already. Creates if doesn't.
