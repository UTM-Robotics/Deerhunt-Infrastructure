from datetime import datetime

from bson import ObjectId

from server.Database import Mongo
from server.Models.Requests.Requests import MatchRequestModel


class MatchRequestManager:
    def __init__(self) -> None:
        self.db = Mongo.requests
        self.request = MatchRequestModel()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    def get_id(self) -> str:
        return self._id

    def pass_data(self, data) -> None:
        # Defender, challenger
        self.request.set_teams([ObjectId(data['team2_id']), ObjectId(data['team1_id'])])
        self.request.set_event(data['event_id'])

    def create_request(self, data) -> bool:
        if not self.find_request(data):
            try:
                self.pass_data(data)
                self.request.set_created_timestamp(str(datetime.utcnow()))
                self.commit()
                return True
            except Exception:
                return False
        else:
            return False

    def find_first_request(self, event_id):
        request = self.db.find_one({'event_id': ObjectId(event_id)})
        if request:
            self.db.delete_one({'event_id': ObjectId(event_id)})
            return request
        return None
    
    def find_request(self, data):
        request = self.db.find_one({'event_id': ObjectId(data['event_id']), 'teams': {
                                   "$all": [ObjectId(data['team1_id']), ObjectId(data['team2_id'])]}})
        if request:
            self._id = request['_id']
            self.pass_data(data)
            self.request.set_created_timestamp(request['created_timestamp'])
            return request
        return None

    def delete_request(self, id) -> bool:
        return self.db.delete_one({'_id': ObjectId(id)})

    def commit(self):
        self.db.insert_one({'event_id': self.request.event_id, 'teams': self.request.teams,
                           'created_timestamp': self.request.created_timestamp})
