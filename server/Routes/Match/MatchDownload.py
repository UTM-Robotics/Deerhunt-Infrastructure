from http import HTTPStatus
from flask import make_response, abort, jsonify, send_file
from flask_restful import Resource, reqparse
from server.Managers.Blob.BlobStorage import BlobStorageModel
from bson import ObjectId
from server.Managers.Matches.MatchResultManager import MatchResultManager
import io

class MatchDownloadRoute(Resource):

    # Note: passing match_id parameters to route
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('match_id', type=str, required=True)
        data = parser.parse_args()
        with MatchResultManager() as matchmanager:
            match = matchmanager.find_match(data['match_id'])
            if match:

                # Get the container , this is common, maybe
                blob_storage = BlobStorageModel()
                container = blob_storage.get_container(match['event_id'])
                if not container:
                    return make_response(jsonify({'message': 'No event container found'}), 404)
                try:
                    blobname = 'match_' + data['match_id']
                    blob = container.get_blob_client(blobname)
                    match_zip = blob.download_blob().readall()
                except Exception as e:
                    return make_response(jsonify({'message': 'Match was won by default(Code doesnt run or code doesnt unzip). No log required'}), 404)
                return send_file(io.BytesIO(match_zip), attachment_filename=f"{blobname}.zip", as_attachment=True)
            else:
                abort(
                        HTTPStatus.BAD_REQUEST,
                        f"Match id does not exist")

