from http import HTTPStatus
from flask import make_response, abort, jsonify
from flask_restful import Resource, reqparse
from bson.json_util import dumps

from server.Managers.Auth.UserManager import User_auth
from server.Managers.Teams.TeamManager import TeamManager


class TeamRoute(Resource):
    parser_get = reqparse.RequestParser()
    parser_get.add_argument('team_name', type=str, required=True, help='This field cannot be left blank')

    parser_put = reqparse.RequestParser()
    parser_put.add_argument('team_name', type=str, required=True, help='This field cannot be left blank')
    parser_put.add_argument('action', type=str, required=True, help='This field cannot be left blank')
    parser_put.add_argument('members', type=list, required=False, help='This field cannot be left blank')

    @User_auth.login_required
    def get(self):
        data = TeamRoute.parser_get.parse_args()
        with TeamManager(data["team_name"]) as teammanager:
            if teammanager.find_team():
                if teammanager.is_part_of_team(User_auth.current_user()):
                    return make_response(
                        dumps(teammanager.team.covert_to_dict()),
                        HTTPStatus.OK,
                    )
                else:
                    abort(HTTPStatus.UNAUTHORIZED, "You must be in the team to access data")
            else:
                abort(HTTPStatus.UNPROCESSABLE_ENTITY, f'Could not fetch team {data["team_name"]}.')

    @User_auth.login_required
    def put(self):
        data = TeamRoute.parser_put.parse_args()
        with TeamManager(data['team_name']) as teammanager:
            if not teammanager.is_part_of_team(User_auth.current_user()):
                return abort(HTTPStatus.UNAUTHORIZED, "You must be in the team to access data")
            if data['action'] == "update" and teammanager.is_owner(User_auth.current_user()):
                result = teammanager.update_members(data['members'].split())
            elif data['action'] == "leave":
                result = teammanager.leave_team(User_auth.current_user())
            if result:
                return make_response(
                    jsonify(
                        {
                            'message': 'Successfully update the team'
                        }),
                    HTTPStatus.OK)
            return abort(HTTPStatus.BAD_REQUEST)
