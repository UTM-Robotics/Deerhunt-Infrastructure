
import traceback
from pymongo import MongoClient

class LeaderboardController:
    ''' Performs all Teams-related logic with Database.'''

    SCRIMMAGE_DELAY_MINUTES = 10
    CHALLENGE_DELAY_MINUTES = 5
    # ChallengeController Errors
    NOT_ON_TEAM_ERROR = 1
    RANK_OUT_OF_BOUNDS_ERROR = 2
    SAME_TEAM_ERROR = 3
    INVALID_TEAM_ERROR = 4
    TIMEOUT_ERROR = 5
    ILLEGAL_ZIP_FILE_ERROR = 6
    def __init__(self, client: MongoClient, database):
        self.client = client
        self.database = database
        self.session = self.client.start_session()
        self.error = None
        self.ret_val = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.session.end_session()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            return False
        return True

    def start_transaction(self):
        ''' Starts the transaction for an object with an activated session'''
        self.session.start_transaction()

    def end_transaction(self):
        ''' Ends the transaction for an object with an activated session'''
        self.session.commit_transaction()

    def get_current_leaderboard(self):
        ''' Gets the current active leaderboard, returns none if it's not there.'''
        self.start_transaction()
        leaderboard = self.database.leaderboard.find_one({"type": "current"}, session=self.session)
        self.end_transaction()
        return leaderboard
    @staticmethod
    def safe_get_team_rank(leaderboard_document, team_name):
        """ Returns infinity if the team is not yet ranked, otherwise, returns
        the first occurence of the team in the leaderboard
        """
        teams = leaderboard_document["teams"]
        if not team_name in teams:
            return float("inf")
        return teams.index(team_name)

    def get_team_rank(leaderboard_document, team_name):
        """ Returns -1 if the team is not yet ranked, otherwise, returns
        the first occurence of the team in the leaderboard
        """
        teams = leaderboard_document["teams"]
        if not team_name in teams:
            return -1
        return teams.index(team_name)

    def get_computation_queue(self):
        """ Returns contests the computation queue"""
        self.start_transaction()
        leaderboard = self.database.submission_queue.find_many({"type": "current"}, session=self.session)
        self.end_transaction()