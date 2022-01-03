import io
import zipfile
from datetime import datetime, timedelta, timezone

import werkzeug
from flask import make_response, request, jsonify, send_file
from flask_restful import Resource, reqparse

from server.Managers.Auth.UserManager import User_auth, UserManager
from server.Managers.Events.AdminEvents import EventsManager
from server.Managers.Teams.TeamsManager import TeamsManager

from server.Managers.Blob.BlobStorage import BlobStorageModel


# TODO: testing and refactoring
class SubmissionsRoute(Resource):
    parser_post = reqparse.RequestParser()
    parser_post.add_argument('team_id', type=str, required=True,
                             help='This field cannot be left blank')
    parser_post.add_argument('event_id', type=str, required=True,
                             help='This field cannot be left blank')
    # parser_post.add_argument('file', type=werkzeug.FileStorage,
    #                          location='files', required=True,
    #                          help='This field cannot be left blank')

    parser_get = reqparse.RequestParser()
    parser_get.add_argument('team_id', type=str, required=True,
                            help='This field cannot be left blank')
    parser_get.add_argument('event_id', type=str, required=True,
                            help='This field cannot be left blank')

    @User_auth.login_required
    def post(self):
        data = SubmissionsRoute.parser_post.parse_args()
        user_file = request.files['file']
        zipfile.is_zipfile(user_file.filename)

        with EventsManager(data['event_id']) as eventsmanager:
            if not eventsmanager.found:
                return make_response(jsonify({'message': 'Event not found'}), 404)

            # TODO: check if event submission is open

        user_email = ''
        with UserManager(User_auth.current_user()) as usermanager:
            if not usermanager.found():
                return make_response(jsonify({'message': 'User not found'}), 404)
            if not usermanager.is_verified():
                return make_response(jsonify({'message': 'Please verify your email first'}), 401)
            user_email = usermanager.user.get_email()
        with TeamsManager() as teamsmanager:
            teamsmanager.get_by_id(data['team_id'])

            if not teamsmanager.is_part_of_team(user_email):
                return make_response(jsonify({'message': 'You are not part of this team'}), 401)

            timestamp = datetime.fromtimestamp(teamsmanager.team.get_last_submission_timestamp(), timezone.utc)
            if timestamp + timedelta(minutes=5) > datetime.now(timezone.utc):
                return make_response(jsonify({'message': 'You can only submit once every 5 minutes'}), 401)

            blob_storage = BlobStorageModel()
            container = blob_storage.get_container(data['event_id'])
            if container is None:
                container = blob_storage.create_container(data['event_id'])

            # delete the last submission somewhere here if you want to

            last_submission = sorted(teamsmanager.team.submissions)[-1]
            last_sub_number = int(last_submission.split('_')[-1])

            new_name = teamsmanager.get_id() + '_' + str(last_sub_number + 1)

            container.upload_blob(new_name, user_file)

    @User_auth.login_required
    def get(self):
        data = SubmissionsRoute.parser_get.parse_args()
        user_email = ''
        with UserManager(User_auth.current_user()) as usermanager:
            if not usermanager.found():
                return make_response(jsonify({'message': 'User not found'}), 404)
            if not usermanager.is_verified():
                return make_response(jsonify({'message': 'Please verify your email first'}), 401)
            user_email = usermanager.user.get_email()
        with TeamsManager() as teamsmanager:
            teamsmanager.get_by_id(data['team_id'])

            if not teamsmanager.is_part_of_team(user_email):
                return make_response(jsonify({'message': 'You are not part of this team'}), 401)

            blob_storage = BlobStorageModel()
            container = blob_storage.get_container(data['event_id'])
            if container is None:
                return make_response(jsonify({'message': 'Event not found'}), 404)

            last_submission = sorted(teamsmanager.team.submissions)[-1]
            blob = container.get_blob_client(last_submission)

            user_submission = blob.download_blob().readall()

            # one of these two might work
            return send_file(blob.download_blob(), attachment_filename=last_submission, as_attachment=True)
            # return send_file(io.BytesIO(user_submission), attachment_filename=last_submission, as_attachment=True)
