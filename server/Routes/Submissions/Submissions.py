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
    parser.add_argument('event_name', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('team_name', type=str, required=True, help='This field cannot be left blank')

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
        with TeamsManager(data["team_name"]) as teamsmanager:
            if not teamsmanager.found:
                return make_response(jsonify({'message': 'Team not found'}), 404)

            if user_email not in teamsmanager.team.get_members():
                return make_response(jsonify({'message': 'You are not part of this team'}), 401)

            with EventsManager(data["event_name"]) as eventsmanager:
                if not eventsmanager.found:
                    return make_response(jsonify({'message': 'Event not found'}), 404)
                if eventsmanager.event.get_id() != teamsmanager.team.get_event_id():
                    return make_response(jsonify({'message': 'Team does not belong to this event'}), 401)

                start_time = datetime.fromisoformat(eventsmanager.event.get_starttime())
                end_time = datetime.fromisoformat(eventsmanager.event.get_endtime())

                if (not start_time < datetime.now() < end_time) or (not eventsmanager.event.get_submission_open()):
                    return make_response(jsonify({'message': 'Submission is not open'}), 401)

                print(teamsmanager.team.covert_to_dict())

                if teamsmanager.team.get_last_submission_timestamp() is not None:
                    print("checking last_submission_timestamp")
                    timestamp = teamsmanager.team.get_last_submission_timestamp()
                    if timestamp + timedelta(minutes=2) > datetime.now():
                        return make_response(jsonify({'message': 'You can only submit once every 5 minutes'}), 401)

                blob_storage = BlobStorageModel()
                container = blob_storage.get_container(str(eventsmanager.event.get_id()))
                if not container:
                    container = blob_storage.create_container(str(eventsmanager.event.get_id()))

                if teamsmanager.team.get_last_submission_timestamp():
                    if len(teamsmanager.team.get_submissions()) > 0:
                        last_submission = teamsmanager.team.get_submissions()[-1]
                        last_sub_number = int(last_submission.split('_')[-1])

                        new_name = str(teamsmanager.team.get_id()) + '_' + str(last_sub_number + 1)
                    else: 
                        new_name = str(teamsmanager.team.get_id()) + "_1"
                else:
                    new_name = str(teamsmanager.team.get_id()) + '_1'

                container.upload_blob(new_name, user_file, overwrite=True)

                teamsmanager.team.set_last_submission_timestamp(datetime.now())
                teamsmanager.team.set_submissions(teamsmanager.team.get_submissions() + [new_name])
                teamsmanager.commit()

                return make_response(jsonify({'message': 'Submission successful'}), 200)

    @User_auth.login_required
    def get(self):
        data = SubmissionsRoute.parser.parse_args()
        with UserManager(User_auth.current_user()) as usermanager:
            if not usermanager.found:
                return make_response(jsonify({'message': 'User not found'}), 404)
            if not usermanager.is_verified():
                return make_response(jsonify({'message': 'Please verify your email first'}), 401)
            user_email = usermanager.user.get_email()
            with TeamsManager(data["team_name"]) as teamsmanager:
                if not teamsmanager.found:
                    return make_response(jsonify({'message': 'Team not found'}), 404)

                if user_email not in teamsmanager.team.get_members():
                    return make_response(jsonify({'message': 'You are not part of this team'}), 401)

                with EventsManager(data["event_name"]) as eventsmanager:
                    if not eventsmanager.found:
                        return make_response(jsonify({'message': 'Event not found'}), 404)
                    if eventsmanager.event.get_id() != teamsmanager.team.get_event_id():
                        return make_response(jsonify({'message': 'Team does not belong to this event'}), 401)

                    blob_storage = BlobStorageModel()
                    container = blob_storage.get_container(str(eventsmanager.event.get_id()))
                    if not container:
                        return make_response(jsonify({'message': 'No submissions found'}), 404)

                    if teamsmanager.team.get_submissions():
                        last_submission = sorted(teamsmanager.team.get_submissions())[-1]
                    else:
                        return make_response(jsonify({'message': 'No submissions found'}), 404)

                    blob = container.get_blob_client(last_submission)

                    user_submission = blob.download_blob().readall()

                    return send_file(io.BytesIO(user_submission), attachment_filename=last_submission, as_attachment=True)
