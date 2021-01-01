from pymongo import MongoClient
from flask import Flask, jsonify, send_from_directory, request, abort, session
from flask_cors import CORS
import traceback
'''
Performs all Teams-related logic with Database.
'''


class GlobalController:
    # GlobalController Errors
    FAILED_STATE_CHANGE = 1

    # Global Document Query
    STATE_DOCUMENT_QUERY = {"file_type": "global"}

    def __init__(self, client, database):
        self.client = client
        self.database = database
        self.error = None
        self.ret_val = None

    def __enter__(self):
        self.session = self.client.start_session()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.session.end_session()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False
        return True

    def get_leaderboard_state(self):
        # Start the session for transaction
        session = self.session
        try:
            session.start_transaction()
            read_state_query = {

            }
            state_document = self.database.globals.find_one(
                read_state_query
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
        # Start the session for transaction
        session = self.session
        try:
            session.start_transaction()
            state_document = self.database.globals.find_one(
                read_state_query
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
        # Start the session for transaction
        session = self.session
        try:
            session.start_transaction()
            state = self.database.globals.find_one(
                STATE_DOCUMENT_QUERY
            )
            if not "leaderboard_enabled" in state:
                session.abort_transaction()
                self.error = self.FAILED_STATE_CHANGE
                return False
            state_data = {"leaderboard_enabled": not state["leaderboard_enabled"]}
            state_result = self.database.globals.update_one(
                STATE_DOCUMENT_QUERY,
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
        # Start the session for transaction
        session = self.session
        try:
            session.start_transaction()
            state = self.database.globals.find_one(
                STATE_DOCUMENT_QUERY
            )
            if not "submit_enabled" in state:
                abort(403)
            state_data = {"submit_enabled": not state["submit_enabled"]}
            state_result = self.database.globals.update_one(
                STATE_DOCUMENT_QUERY,
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
