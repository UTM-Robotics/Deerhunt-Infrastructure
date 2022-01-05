from http import HTTPStatus
from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Matches.MatchRequestManager import MatchRequestManager
from server.config import Configuration


class ConsumerRoute(Resource):
    def check_auth(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True,
                            help='Must provide secret token to use this api')
        data = parser.parse_args()
        if data['token'] != Configuration.CONSUMER_TOKEN:
            return abort(HTTPStatus.UNAUTHORIZED)

    def post(self):
        self.check_auth()
        parser = reqparse.RequestParser()
        parser.add_argument('teams', type=str, required=True, action="append")
        parser.add_argument('event_id', type=str, required=True)
        data = parser.parse_args()
        with MatchRequestManager() as requestmanager:
            if requestmanager.create_request(data):
                return make_response(jsonify({'message': 'Successfully created a match request'}), HTTPStatus.OK)
            else:
                raise SystemError("Error occurs when create request")

    # Note: passing token, event_id parameters to route
    def get(self):
        self.check_auth()
        parser = reqparse.RequestParser()
        parser.add_argument('event_id', type=str, required=True)
        data = parser.parse_args()
        with MatchRequestManager() as requestmanager:
            return requestmanager.find_first_request(data['event_id'])

    def delete(self):
        self.check_auth()
        parser = reqparse.RequestParser()
        parser.add_argument('request_id', type=str, required=True)
        data = parser.parse_args()
        with MatchRequestManager() as requestmanager:
            if requestmanager.delete_request(data['request_id']):
                return make_response(jsonify({'message': 'Request deleted'}), HTTPStatus.OK)
            return abort(HTTPStatus.BAD_REQUEST)
