from http import HTTPStatus

from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Teams.TeamsManager import TeamsManager
from server.Managers.Auth.UserManager import UserManager

from server.Managers.Auth.UserManager import User_auth


class TeamsRoute(Resource):

    # flask parser for post request
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cannot be left blank')

    @User_auth.login_required
    def post(self):
        email = User_auth.current_user()
        data = TeamsRoute.parser.parse_args()
        # with UserManager(email) as usermanager:
        #     pass # check that user isn't part of team
        with TeamsManager(data['name']) as teamsmanager:
            result = teamsmanager.create_team(email)
            if result:
                return make_response(jsonify({'message': 'New Team Created'}))
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'Team name taken')
            
