from datetime import datetime

from bson import ObjectId

from server.Database import Mongo
from server.Models.Matches.Matches import MatchRequestModel


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
        if data['teams']:
            self.request.set_teams(data['teams'])
        if data['event_id']:
            self.request.set_event(data['event_id'])
        if data['created_timestamp']:
            self.request.set_created_timestamp(data['created_timestamp'])

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
            self._id = request['_id']
            self.pass_data(request)
            return self.request.covert_to_dict()
        return None
    
    def find_request(self, data):
        request = self.db.find_one({'event_id': ObjectId(data['event_id']), 'teams': {
                                   "$all": [ObjectId(data['teams'][0]), ObjectId(data['teams'][1])]}})
        if request:
            self._id = request['_id']
            self.pass_data(data)
            return request
        return None

    def delete_request(self, id) -> bool:
        return self.db.delete_one({'_id': ObjectId(id)})

    def commit(self) -> None:
        data = self.request.covert_to_dict()
        self.db.insert_one(data)
