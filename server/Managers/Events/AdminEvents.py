import jwt

from datetime import datetime, timedelta

from server.Database import Mongo
from server.Models.Events.Events import EventsModel

from server.config import Configuration


class EventsManager:
    def __init__(self, name=None):
        self.db = Mongo.events
        self.event = EventsModel(name)

    def __enter__(self):
        # self.session = Mongo.start_session()
        result = self.find_event()
        if self.event.get_name() and result:
            self.event.set_name(result['name'])
            self.event.set_game(result['game'])
            self.event.set_starttime(result['starttime'])
            self.event.set_endtime(result['endtime'])
            self.event.set_created_timestamp(result['created_timestamp'])
            self.found = True
        else:
            self.all_events = result
            self.found = False
        return self

    def __exit__(self, type, value, tb):
        # self.session.end_session()
        pass

    def find_event(self):
        '''
        If this class was called without a name, it returns all events in a list.
        If called with a name but doesn't find the event, returns None.
        if called with a name and finds the event, returns dict of event.
        '''
        if self.event.get_name():
            return self.db.find_one({'name': self.event.get_name()})
        all_events = list()
        for i in self.db.find():
            all_events.append(i)
        return all_events

    def get_events(self):
        return self.all_events

    def create_event(self, game, starttime, endtime):
        if not self.found and not self.all_events:
            self.event.set_game(game)
            self.event.set_starttime("")
            self.event.set_endtime("")
            self.event.set_created_timestamp(str(datetime.utcnow()))
            self.commit()
            return True
        return False

    def delete(self):
        if self.found:
            if self.db.delete_one({'name': self.event.get_name()}):
                return True
            else:
                return False
        return False

    def get_event_data(self):
        return self.db.find_one({'name': self.event.get_name()}) # for now
        # return self.event.covert_to_dict() <- the one it should be.

    def commit(self):
        query = {'name': self.event.get_name()}
        data = self.event.covert_to_dict()
        if self.found:
            self.db.update_one(query, {'$set': data })
        else:
            self.db.update_one(query, {"$setOnInsert": data}, upsert=True)
