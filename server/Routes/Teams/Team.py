from http import HTTPStatus
from flask import make_response, abort, jsonify
from flask_restful import Resource, request
from bson.json_util import dumps

from server.Managers.Auth.UserManager import User_auth
from server.Managers.Teams.TeamManager import TeamManager


class TeamRoute(Resource):
    @User_auth.login_required
    def get(self):
        args = request.args
        with TeamManager(args["name"]) as teammanager:
            if teammanager.find_team():
              if teammanager.is_part_of_team(User_auth.current_user()):
                return make_response(
                    dumps(teammanager.team.covert_to_dict()),
                    HTTPStatus.OK,
                )
              else:
                abort(HTTPStatus.UNAUTHORIZED, "You must be in the team to access data")
            else:
                abort(HTTPStatus.UNPROCESSABLE_ENTITY, f'Could not fetch team {args["name"]}.')

    @User_auth.login_required
    def put(self):
      # Note: Content-Type must be application/json. Need JSON object in body.
        args = request.get_json(force=True)
        with TeamManager(args['name']) as teammanager:
            if not teammanager.is_part_of_team(User_auth.current_user()):
                return abort(HTTPStatus.UNAUTHORIZED, "You must be in the team to access data")
            if args['action'] == "update" and teammanager.is_owner(User_auth.current_user()):
                result = teammanager.update_members(args['members'].split())
            elif args['action'] == "leave":
                result = teammanager.leave_team(User_auth.current_user())
            if result:
                return make_response(
                    jsonify(
                        {
                            'message': 'Successfully update the team'
                        }),
                    HTTPStatus.OK)
            return abort(HTTPStatus.BAD_REQUEST)
