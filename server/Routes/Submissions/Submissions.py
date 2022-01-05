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
from bson.objectid import ObjectId


# TODO: testing and refactoring
class SubmissionsRoute(Resource):
    parser_post = reqparse.RequestParser()
    parser_post.add_argument('team_id', type=str, required=True,
                             help='This field cannot be left blank')
    # parser_post.add_argument('event_id', type=str, required=True,
    #                          help='This field cannot be left blank')
    # parser_post.add_argument('file', type=werkzeug.FileStorage,
    #                          location='files', required=True,
    #                          help='This field cannot be left blank')

    parser_get = reqparse.RequestParser()
    parser_get.add_argument('team_id', type=str, required=True,
                            help='This field cannot be left blank')
    # parser_get.add_argument('event_id', type=str, required=True,
    #                         help='This field cannot be left blank')

    @User_auth.login_required
    def post(self):
        data = SubmissionsRoute.parser_post.parse_args()
        user_file = request.files['file']
        # print(user_file)
        # print(data)
        is_zip = user_file.filename.endswith('.zip')
        # print(is_zip)

        if not is_zip:
            return make_response(jsonify({'message': 'File must be a zip file'}), 400)

        with UserManager(User_auth.current_user()) as usermanager:
            if not usermanager.found:
                return make_response(jsonify({'message': 'User not found'}), 404)
            if not usermanager.is_verified():
                return make_response(jsonify({'message': 'Please verify your email first'}), 401)
            user_email = usermanager.user.get_email()
        with TeamsManager() as teamsmanager:
            teams = teamsmanager.find_teams([ObjectId(data['team_id'])])
            print(teams)
            print(type(teams))
            if not teams:
                return make_response(jsonify({'message': 'Team not found'}), 404)
            team = teams[0]
            print("team-type", type(team))
            print(team)

            teamsmanager.team.set_name(team['name'])
            teamsmanager.team.set_id(team['_id'])
            teamsmanager.team.set_owner(team['owner'])
            teamsmanager.team.set_members(team['members'])
            teamsmanager.team.set_event_id(team['event_id'])
            teamsmanager.team.set_last_submission_timestamp(team['last_submission_timestamp'])
            teamsmanager.team.set_created_timestamp(team['created_timestamp'])
            teamsmanager.found = True

            if user_email not in team['members']:
                return make_response(jsonify({'message': 'You are not part of this team'}), 401)

            # print(str(team['event_id']))
            with EventsManager() as eventsmanager:
                events = eventsmanager.find_event()
                filtered_events = [event for event in events if event['_id'] == ObjectId(team['event_id'])]
                if not filtered_events:
                    return make_response(jsonify({'message': 'Event not found'}), 404)

                event = filtered_events[0]
                # print(event)
                # TODO: check if event submission is open
            if team['last_submission_timestamp'] is not None:
                print("checking last_submission_timestamp")
                timestamp = team['last_submission_timestamp']
                if timestamp + timedelta(minutes=5) > datetime.now():
                    return make_response(jsonify({'message': 'You can only submit once every 5 minutes'}), 401)

            blob_storage = BlobStorageModel()
            container = blob_storage.get_container(str(event['_id']))
            # print("existing-container", container)
            if not container:
                container = blob_storage.create_container(str(event['_id']))
                # print("new-container", container)

            if team['submissions']:
                last_submission = sorted(team['submissions'])[-1]
                last_sub_number = int(last_submission.split('_')[-1])

                new_name = str(teamsmanager.team.get_id()) + '_' + str(last_sub_number + 1)
            else:
                new_name = str(teamsmanager.team.get_id()) + '_1'

            container.upload_blob(new_name, user_file)

            teamsmanager.team.set_last_submission_timestamp(datetime.now())
            teamsmanager.team.set_submissions(team['submissions'] + [new_name])
            teamsmanager.commit()

    @User_auth.login_required
    def get(self):
        data = SubmissionsRoute.parser_get.parse_args()
        user_email = ''
        with UserManager(User_auth.current_user()) as usermanager:
            if not usermanager.found:
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
