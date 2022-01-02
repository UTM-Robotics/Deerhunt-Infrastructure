import os
import zipfile
from datetime import datetime, timedelta, timezone
from typing import List

import werkzeug
from flask import make_response, request, abort, jsonify, send_file
from flask_restful import Resource, reqparse

from server.Managers.Auth.UserManager import User_auth, UserManager
from server.Managers.Events.AdminEvents import EventsManager
from server.Managers.Teams.TeamsManager import TeamsManager
from server.Models.User import GeneralUser

from server.Managers.Blob.BlobStorage import BlobStorageModel


class SubmissionsRoute(Resource):
    parser_post = reqparse.RequestParser()
    parser_post.add_argument('team_id', type=str, required=True,
                             help='This field cannot be left blank')
    parser_post.add_argument('event_id', type=str, required=True,
                             help='This field cannot be left blank')
    parser_post.add_argument('file', type=werkzeug.FileStorage,
                             location='files', required=True,
                             help='This field cannot be left blank')

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

            # TODO: upload the file to asure and update the team submission timestamp
            blob_storage = BlobStorageModel()
            container = blob_storage.get_container(data['event_id'])
            if container is None:
                container = blob_storage.create_container(data['event_id'])

            # # finds last submission of the team
            # all_submissions = blob_storage.list_blobs_in_container(data['event_id'])
            # if not all_submissions:
            #     print('container fetch error')
            #     return make_response(jsonify({'message': 'An error has occurred'}), 500)
            #
            # # formatted as "{teamID}_{submission_number}"
            # user_submissions: List[str] = [blob for blob in all_submissions if blob.name.startswith(data['team_id'])]
            # user_submissions.sort()
            # last_submission = user_submissions[-1]

            # delete the last submission somewhere here if you want to

            last_submission = sorted(teamsmanager.team.submissions)[-1]
            last_sub_number = int(last_submission.split('_')[-1])

            new_name = teamsmanager.get_id() + '_' + str(last_sub_number + 1)

            container.upload_blob(new_name, user_file)

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

            # TODO: Make this like the post route
            #
            # blob_storage = BlobStorageModel()
            # container = blob_storage.get_container(data['event_id'])
            # if container is None:
            #     container = blob_storage.create_container(data['event_id'])
            #
            # sub = list(blob_storage.list_blobs_in_container(data['event_id']))
            # print(sub)
            #
            # sub = [name for name in sub if name.startswith(teamsmanager.team.get_uuid())]
            # sub.sort()
            #
            # last_sub = sub[-1]
            #
            # file = blob_storage.get_blob(data['event_id'], last_sub)
            #
            # if file:
            #     return send_file(file, mimetype='application/zip')
            # else:
            #     return make_response(jsonify({'message': 'No submission found'}), 404)