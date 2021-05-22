import traceback
from datetime import datetime
from pymongo import MongoClient

class GlobalController:
    """
    Performs all global_state logic with Database.
    Enables all instances of the API to act as one instance.
    """
    # GlobalController Errors
    FAILED_STATE_CHANGE = 1

    # Global Document Query
    STATE_DOCUMENT_QUERY = {"file_type": "global"}

    def __init__(self, client: MongoClient, database):
        self.client = client
        self.database = database
        self.error = None
        self.ret_val = None
        self.session = self.client.start_session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.session.end_session()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            return False
        return True

    def end_session(self):
        ''' Ends an already started session. Does not commit.'''
        self.session.end_session()

    def init_state(self):
        try:
            col = self.database.globals
            self.database.globals.drop()
            col = self.database.globals
            col.insert_one(
                {
                    "file_type":"global",
                    "leaderboard_enabled": False,
                    "submit_enabled": False,
                    "server_start_time": datetime.utcnow()
                }
            )
        except (Exception) as exc:
            print(exc)
            self.error = self.FAILED_STATE_CHANGE
            return False
        return True

    def get_leaderboard_state(self):
        session = self.session
        try:
            session.start_transaction()

            state_document = self.database.globals.find_one(
                self.STATE_DOCUMENT_QUERY,
                session=session
            )
            if not "leaderboard_enabled" in state_document:
                self.error = self.FAILED_STATE_CHANGE
                return False
            session.commit_transaction()
            self.ret_val = state_document["leaderboard_enabled"]
        except (Exception) as exc:
            print(exc)
            session.abort_transaction()
            self.error = self.FAILED_STATE_CHANGE
            return False
        return True

    def get_submit_state(self):
        '''Toggles whether the leaderboard is enabled or not'''
        session = self.session
        try:
            session.start_transaction()
            state_document = self.database.globals.find_one(
                self.STATE_DOCUMENT_QUERY,
                session=session
            )
            if not "submit_enabled" in state_document:
                self.error = self.STATE_DOCUMENT_QUERY
                return False
            session.commit_transaction()
            self.ret_val = state_document["submit_enabled"]
        except (Exception) as exc:
            print(exc)
            session.abort_transaction()
            self.error = self.FAILED_STATE_CHANGE
            return False
        return True

    def leaderboard_toggle(self):
        '''Toggles whether the leaderboard is enabled or not'''
        session = self.session
        try:
            session.start_transaction()
            state = self.database.globals.find_one(
                self.STATE_DOCUMENT_QUERY,
                session=session
            )
            if not "leaderboard_enabled" in state:
                session.abort_transaction()
                self.error = self.FAILED_STATE_CHANGE
                return False
            state_data = {"$set":{"leaderboard_enabled": not state["leaderboard_enabled"]}}
            state_result = self.database.globals.update_one(
                self.STATE_DOCUMENT_QUERY,
                state_data,
                session=session
            )
            if state_result.modified_count != 1:
                self.session.abort_transaction()
                self.error = self.FAILED_STATE_CHANGE
                return False
            session.commit_transaction()
            self.ret_val = not state["leaderboard_enabled"]
        except (Exception) as exc:
            print(exc)
            session.abort_transaction()
            self.error = self.FAILED_STATE_CHANGE
            return False
        return True

    def submit_toggle(self):
        '''
            Negates the global state value for submission enable.
        '''
        session = self.session
        try:
            session.start_transaction()
            state = self.database.globals.find_one(
                self.STATE_DOCUMENT_QUERY,
                session=session
            )
            if not "submit_enabled" in state:
                self.session.abort_transaction()
                self.error = self.FAILED_STATE_CHANGE
                return False
            state_data = {"$set":{"submit_enabled": not state["submit_enabled"]}}
            state_result = self.database.globals.update_one(
                self.STATE_DOCUMENT_QUERY,
                state_data,
                session=session
            )
            if state_result.modified_count != 1:
                self.session.abort_transaction()
                self.error = self.FAILED_STATE_CHANGE
                return False
            session.commit_transaction()
            self.ret_val = not state["submit_enabled"]
        except (Exception) as exc:
            print(exc)
            session.abort_transaction()
            self.error = self.FAILED_STATE_CHANGE
            return False
        return True

    @staticmethod
    def is_submit_locked(self, client, database):
        with GlobalController(client, database) as globals_api:
            if not globals_api.get_submit_state():
               raise Exception("Is Submit Failed")
        return globals_api.ret_val
