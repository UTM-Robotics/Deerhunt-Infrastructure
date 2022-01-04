from http import HTTPStatus
from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Matches.MatchResultManager import MatchResultManager
from server.config import Configuration


class MatchRoute(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True,
                            help='Must provide secret token to use this api')
        parser.add_argument('event_id', type=str, required=True)
        parser.add_argument('winner_id', type=str, required=True)
        parser.add_argument('loser_id', type=str, required=True)
        data = parser.parse_args()
        if data['token'] != Configuration.CONSUMER_TOKEN:
            return abort(HTTPStatus.UNAUTHORIZED)
        with MatchResultManager() as matchmanager:
            if matchmanager.create_match(data):
                return make_response(jsonify({'message': 'Successfully created a match record'}), HTTPStatus.OK)
            else:
                raise SystemError("Error occurs when create match record")

    # Note: passing match_id parameters to route
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('match_id', type=str, required=True)
        data = parser.parse_args()
        with MatchResultManager() as matchmanager:
            return matchmanager.find_match(data['match_id'])
