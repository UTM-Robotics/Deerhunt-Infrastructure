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
    parser = reqparse.RequestParser()
    parser.add_argument('team_id', type=str, required=True, help='This field cannot be left blank')

    @User_auth.login_required
    def post(self):
        data = SubmissionsRoute.parser.parse_args()
        user_file = request.files['file']
        is_zip = user_file.filename.endswith('.zip')

        if not is_zip:
            return make_response(jsonify({'message': 'File must be a zip file'}), 400)

        with UserManager(User_auth.current_user()) as usermanager:
            if not usermanager.found:
                return make_response(jsonify({'message': 'User not found'}), 404)
            if not usermanager.is_verified():
                return make_response(jsonify({'message': 'Please verify your email first'}), 401)
            user_email = usermanager.user.get_email()
        with TeamsManager() as teamsmanager:
            try:
                id_object = ObjectId(data['team_id'])
            except:
                return make_response(jsonify({'message': 'Invalid team id'}), 400)

            teams = teamsmanager.find_teams([id_object])
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

            with EventsManager() as eventsmanager:
                events = eventsmanager.find_event()
                filtered_events = [event for event in events if event['_id'] == ObjectId(team['event_id'])]
                if not filtered_events:
                    return make_response(jsonify({'message': 'Event not found'}), 404)

                event = filtered_events[0]

                start_time = datetime.fromisoformat(event['starttime'])
                end_time = datetime.fromisoformat(event['endtime'])

                if (not start_time < datetime.now() < end_time) or (not event['submission_open']):
                    return make_response(jsonify({'message': 'Submission is not open'}), 401)

            if team['last_submission_timestamp'] is not None:
                print("checking last_submission_timestamp")
                timestamp = team['last_submission_timestamp']
                if timestamp + timedelta(minutes=5) > datetime.now():
                    return make_response(jsonify({'message': 'You can only submit once every 5 minutes'}), 401)

            blob_storage = BlobStorageModel()
            container = blob_storage.get_container(str(event['_id']))
            if not container:
                container = blob_storage.create_container(str(event['_id']))

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
        data = SubmissionsRoute.parser.parse_args()
        with UserManager(User_auth.current_user()) as usermanager:
            if not usermanager.found:
                return make_response(jsonify({'message': 'User not found'}), 404)
            if not usermanager.is_verified():
                return make_response(jsonify({'message': 'Please verify your email first'}), 401)
            user_email = usermanager.user.get_email()
        with TeamsManager() as teamsmanager:
            try:
                id_object = ObjectId(data['team_id'])
            except:
                return make_response(jsonify({'message': 'Invalid team id'}), 400)

            teams = teamsmanager.find_teams([id_object])
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

            with EventsManager() as eventsmanager:
                events = eventsmanager.find_event()
                filtered_events = [event for event in events if event['_id'] == ObjectId(team['event_id'])]
                if not filtered_events:
                    return make_response(jsonify({'message': 'Event not found'}), 404)

                event = filtered_events[0]

            blob_storage = BlobStorageModel()
            container = blob_storage.get_container(str(event['_id']))
            if not container:
                return make_response(jsonify({'message': 'No submissions found'}), 404)

            if team['submissions']:
                last_submission = sorted(team['submissions'])[-1]
            else:
                return make_response(jsonify({'message': 'No submissions found'}), 404)

            blob = container.get_blob_client(last_submission)

            user_submission = blob.download_blob().readall()

            # one of these two might work
            # return send_file(blob.download_blob(), attachment_filename=last_submission+".zip", as_attachment=True)
            return send_file(io.BytesIO(user_submission), attachment_filename=last_submission, as_attachment=True)
