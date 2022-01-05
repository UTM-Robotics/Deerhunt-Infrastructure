from datetime import time
from http import HTTPStatus
from flask import make_response, abort, jsonify
from flask_restful import Resource, reqparse
from bson.json_util import dumps

from server.Managers.Teams.TeamsManager import TeamsManager
from server.Managers.Auth.UserManager import User_auth


class TeamsRoute(Resource):
    @User_auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                        help='This field cannot be left blank')
        parser.add_argument('event_id', type=str, required=True,
                            help='This field cannot be left blank')
        data = TeamsRoute.parser.parse_args()
        with TeamsManager(data['name']) as teamsmanager:
            result = teamsmanager.create_team(data, User_auth.current_user())
            if result:
                return make_response(
                    jsonify(
                        {
                            "message": "Team created successfuly."
                        }
                    ),
                    HTTPStatus.CREATED,
                )
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, "Team with provided name already exists.")


    @User_auth.login_required
    def get(self):
        with TeamsManager() as teamsmanager:
            result = teamsmanager.get_teams(User_auth.current_user())
            if result:
                return make_response(
                    dumps(result),
                    HTTPStatus.OK,
                )
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'Could not fetch teams of user.')


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
