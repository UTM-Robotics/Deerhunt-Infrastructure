import zipfile
from datetime import datetime, timedelta, timezone
import werkzeug
from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Auth.UserManager import User_auth, UserManager
from server.Managers.Teams.TeamsManager import TeamsManager
from server.Models.User import GeneralUser

from server.Managers.Blob.BlobStorage import BlobStorageModel


class SubmissionsRoute(Resource):
    parser_post = reqparse.RequestParser()
    parser_post.add_argument('team_name', type=str, required=True,
                             help='This field cannot be left blank')
    parser_post.add_argument('event_id', type=str, required=True,
                             help='This field cannot be left blank')
    parser_post.add_argument('file', type=werkzeug.datastructures.FileStorage,
                             location='files', required=True,
                             help='This field cannot be left blank')

    parser_get = reqparse.RequestParser()
    parser_get.add_argument('team_name', type=str, required=True,
                            help='This field cannot be left blank')
    parser_get.add_argument('event_id', type=str, required=True,
                            help='This field cannot be left blank')

    @User_auth.login_required
    def post(self):
        data = SubmissionsRoute.parser_post.parse_args()
        user_file = data['file']
        zipfile.is_zipfile(user_file)

        # TODO: check if submission is open

        user_email = ''
        with UserManager(User_auth.current_user()) as usermanager:
            if not usermanager.is_verified():
                return make_response(jsonify({'message': 'Please verify your email first'}), 401)
            user_email = usermanager.user.get_email()
        with TeamsManager(data['team_name']) as teamsmanager:
            if not teamsmanager.is_part_of_team(user_email):
                return make_response(jsonify({'message': 'You are not part of this team'}), 401)

            timestamp = datetime.fromtimestamp(teamsmanager.team.get_last_submission_timestamp(), timezone.utc)
            if timestamp + timedelta(minutes=5) > datetime.now(timezone.utc):
                return make_response(jsonify({'message': 'You can only submit once every 5 minutes'}), 401)

            # TODO: upload the file to asure and update the team submission timestamp


    @User_auth.login_required
    def get(self):

        data = SubmissionsRoute.parser_get.parse_args()
        with UserManager(User_auth.current_user()) as usermanager:
            if not usermanager.is_verified():
                return make_response(jsonify({'message': 'Please verify your email first'}), 401)
            user_email = usermanager.user.get_email()
        with TeamsManager(data['team_name']) as teamsmanager:
            if not teamsmanager.is_part_of_team(user_email):
                return make_response(jsonify({'message': 'You are not part of this team'}), 401)

            # TODO: get the last submission of the user/team
