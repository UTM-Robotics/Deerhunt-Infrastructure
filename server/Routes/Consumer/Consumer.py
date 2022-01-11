from datetime import datetime
from http import HTTPStatus
from flask import make_response, abort, jsonify
from bson.json_util import dumps, ObjectId
from flask_restful import Resource, reqparse
from server.Managers.Auth.UserManager import User_auth

from server.Managers.Matches.MatchRequestManager import MatchRequestManager
from server.Managers.Events.AdminEvents import EventsManager
from server.Managers.Teams.TeamsManager import TeamsManager
from server.config import Configuration


class ConsumerRoute(Resource):
    def check_auth(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True,
                            help='Must provide secret token to use this api')
        data = parser.parse_args()
        if data['token'] != Configuration.CONSUMER_TOKEN:
            return abort(HTTPStatus.UNAUTHORIZED)

    @User_auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('team1_id', type=str, required=True)
        parser.add_argument('team2_id', type=str, required=True)
        parser.add_argument('name', type=str, required=True)
        data = parser.parse_args()
        with EventsManager(data['name']) as eventmanager:
            eventdata = eventmanager.find_event()
            data['event_id'] = eventdata['_id']
            with TeamsManager() as teamsmanager:
                defending_team = teamsmanager.find_team_by_id(ObjectId(data['team2_id']))
                if not defending_team:
                    abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'Invalid defending team submission')
            with TeamsManager() as teamsmanager:
                challenging_team = teamsmanager.find_team_by_id(ObjectId(data['team1_id']))
                if challenging_team['last_challenge_timestamp'] == None:
                    with MatchRequestManager() as requestmanager:# this is duplicate code, need a function
                        if requestmanager.create_request(data):
                            challenging_team['last_challenge_timestamp'] = str(datetime.utcnow())
                            teamsmanager.commit_data(challenging_team)
                            return make_response(jsonify({'message': 'Successfully created a match request'}), HTTPStatus.OK)
                        else:
                            raise SystemError("Error occurs when create request")
                else:
                    last_challenge = datetime.strptime(
                        challenging_team['last_challenge_timestamp'], "%Y-%m-%d %H:%M:%S.%f"
                    )
                    curr_time = datetime.utcnow()
                    time_delta = curr_time - last_challenge
                    if time_delta.seconds >= 1:#300:
                        with MatchRequestManager() as requestmanager:
                            if requestmanager.create_request(data):
                                challenging_team['last_challenge_timestamp'] = str(datetime.utcnow())
                                teamsmanager.commit_data(challenging_team)
                                return make_response(jsonify({'message': 'Successfully created a match request'}), HTTPStatus.OK)
                            else:
                                print("An error may have occurred. Like")
                                abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'There is currently a request in queue, please wait.')
                    else:
                        abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'Need to wait 5 minutes till you can challenge again.')

    # Note: passing token, event_id parameters to route
    def get(self):
        self.check_auth()
        parser = reqparse.RequestParser()
        parser.add_argument('event_id', type=str, required=True)
        data = parser.parse_args()
        with MatchRequestManager() as requestmanager:
            result = requestmanager.find_first_request(data['event_id'])
            
            if result:
                result["_id"] = str(result["_id"])
                return make_response(dumps([result]), HTTPStatus.OK)
            return make_response(jsonify({"message": "No match found"}), HTTPStatus.UNPROCESSABLE_ENTITY)
    def delete(self):
        self.check_auth()
        parser = reqparse.RequestParser()
        parser.add_argument('request_id', type=str, required=True)
        data = parser.parse_args()
        with MatchRequestManager() as requestmanager:
            if requestmanager.delete_request(data['request_id']):
                return make_response(jsonify({'message': 'Request deleted'}), HTTPStatus.OK)
            return abort(HTTPStatus.BAD_REQUEST)
