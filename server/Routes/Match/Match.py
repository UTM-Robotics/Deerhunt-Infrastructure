from http import HTTPStatus
from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse
from bson.json_util import dumps
from server.Managers.Blob.BlobStorage import BlobStorageModel
from server.Managers.Events.AdminEvents import EventsManager
from server.Managers.Leaderboard.LeaderboardManager import LeaderboardManager

from server.Managers.Matches.MatchResultManager import MatchResultManager
from server.Managers.Teams.TeamsManager import TeamsManager
from server.config import Configuration


class MatchRoute(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "token",
            type=str,
            required=True,
            help="Must provide secret token to use this api",
        )
        parser.add_argument("event_id", type=str, required=True)
        parser.add_argument("winner_id", type=str, required=True)
        parser.add_argument("loser_id", type=str, required=True)
        data = parser.parse_args()
        match_file = request.files["file"]
        if not match_file.filename.endswith(".zip"):
            return make_response(jsonify({"message": "File must be a zip file"}), 400)
        if data["token"] != Configuration.CONSUMER_TOKEN:
            return abort(HTTPStatus.UNAUTHORIZED)
        with MatchResultManager() as matchmanager:
            if matchmanager.create_match(data):
                with LeaderboardManager() as leaderboardmanager:
                    all_team_ids = leaderboardmanager.get_leaderboard(data['event_id'])
                    leaderboardmanager.update_leaderboard(all_team_ids, data)
                blob_storage = BlobStorageModel()
                container = blob_storage.get_container(data["event_id"])
                if not container:
                    container = blob_storage.create_container(data["event_id"])
                name = f"match_{matchmanager.get_id()}"
                container.upload_blob(name, match_file)
                return make_response(
                    jsonify({"message": "Successfully created a match record"}),
                    HTTPStatus.OK,
                )
            else:
                raise SystemError("Error occurs when create match record")

    # Note: passing match_id parameters to route
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("event_name", type=str, required=True)
        parser.add_argument("match_id", type=str, required=False)
        data = parser.parse_args()
        with EventsManager(data["event_name"]) as eventmanager:
            if not eventmanager.found:
                return make_response(
                    jsonify({"message": "No event with that name exists."}),
                    HTTPStatus.NOT_FOUND,
                )
            event_id = eventmanager.event.get_id()
        with MatchResultManager() as matchmanager:
            if event_id:
                result = matchmanager.find_all_matches(event_id)
                with TeamsManager() as teamsmanager:
                    results = []
                    val = next(result, None)
                    while len(results) < 30 and val:
                        results.append(val)
                        val = next(result, None)
                    for match in result:
                        loser = teamsmanager.find_team_by_id(match['loser_id'])
                        match['loser'] = loser['name']
                        winner = teamsmanager.find_team_by_id(match['winner_id'])
                        match['winner'] = winner['name']
                    return make_response(dumps(result), HTTPStatus.OK)
            else:
                result = matchmanager.find_match(event_id)
                return make_response(dumps(result), HTTPStatus.OK)
