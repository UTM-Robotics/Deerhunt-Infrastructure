from datetime import datetime
from http import HTTPStatus
from flask import make_response, abort, jsonify, send_file
from bson.json_util import dumps, ObjectId
from flask_restful import Resource, reqparse
from server.Managers.Auth.UserManager import User_auth
import io

from server.Managers.Matches.MatchRequestManager import MatchRequestManager
from server.Managers.Events.AdminEvents import EventsManager
from server.Managers.Teams.TeamsManager import TeamsManager
from server.Models.Teams.Teams import TeamsModel
from server.config import Configuration
from server.Managers.Blob.BlobStorage import BlobStorageModel


class ConsumerDownloadRoute(Resource):
    def check_auth(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True,
                            help='Must provide secret token to use this api')
        data = parser.parse_args()
        if data['token'] != Configuration.CONSUMER_TOKEN:
            return abort(HTTPStatus.UNAUTHORIZED)

    def get(self):
        ''' Given a team id, allows a consumer to retrieve that team's submission zip.'''
        self.check_auth()
        parser = reqparse.RequestParser()
        parser.add_argument('team_id', type=str, required=True)
        parser.add_argument('event_name', type=str, required=True)
        data = parser.parse_args()
        with TeamsManager() as teamsmanager:
            team = teamsmanager.find_team_by_id(ObjectId(data['team_id']))
            if not team:
                return make_response(jsonify({'message': 'Team not found'}), 404)
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
                return send_file(io.BytesIO(user_submission), attachment_filename="submission.zip", as_attachment=True)
