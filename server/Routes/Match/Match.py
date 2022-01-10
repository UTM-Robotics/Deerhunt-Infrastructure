from http import HTTPStatus
from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse
from server.Managers.Blob.BlobStorage import BlobStorageModel
from server.Managers.Leaderboard.LeaderboardManager import LeaderboardManager

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
        match_file = request.files['file']
        if not match_file.filename.endswith('.zip'):
            return make_response(jsonify({'message': 'File must be a zip file'}), 400)
        if data['token'] != Configuration.CONSUMER_TOKEN:
            return abort(HTTPStatus.UNAUTHORIZED)
        with MatchResultManager() as matchmanager:
            if matchmanager.create_match(data):
                # with LeaderboardManager() as leaderboardmanager:
                #     all_team_ids = leaderboardmanager.get_leaderboard(data['event_id'])
                #     leaderboardmanager.update_leaderboard(all_team_ids, data)
                blob_storage = BlobStorageModel()
                container = blob_storage.get_container(data['event_id'])
                if not container:
                    container = blob_storage.create_container(data['event_id'])
                name = f'match_{matchmanager.get_id()}'
                container.upload_blob(name, match_file)
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

