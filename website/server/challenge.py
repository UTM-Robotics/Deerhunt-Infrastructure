''' Handles all challenge and scrimmage controls.'''

import traceback
from pymongo import MongoClient

from teams import TeamController
from storage import StorageAPI
from game_runner import GameController
class ChallengeController:
    ''' Performs all Teams-related logic with Database.'''

    # ChallengeController Errors
    NOT_ON_TEAM_ERROR = 1
    RANK_OUT_OF_BOUNDS_ERROR = 2
    SAME_TEAM_ERROR = 3
    INVALID_TEAM_ERROR = 4
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

    def can_challenge(self, team, target_rank):
        '''Returns whether or not the challenge can be performed by the user to another team.'''
        return True

    def queue_challenge(self, team, target_rank):
        '''Adds the team to the challenge queue against team at the target rank'''
        # get user team
        # add team to challenge queue.

    def do_scrimmage(self, username, target_rank):
        '''Performs a scrimmage between the user's team and another team at the target rank
            Returns the game_id of the scrimmage.
        '''
        self.start_transaction()
        team_api = TeamController(self.client, self.database, input_session=self.session)
        user_team = team_api.get_user_team(username)
        if not user_team:
            self.error = self.NOT_ON_TEAM_ERROR
            return False

        # get team at target rank
        current_leaderboard = self.database.leaderboards.find_one({"type": "current"})
        if len(current_leaderboard["teams"]) < target_rank:
            self.error = self.RANK_OUT_OF_BOUNDS_ERROR
            return False
        target_team_name = current_leaderboard["team"][target_rank]
        target_team = team_api.get_team(target_team_name)
        # Cannot compete
        if not target_team:
            self.error = self.INVALID_TEAM_ERROR
            return False
        if target_team["name"] == user_team["name"]:
            self.error = self.SAME_TEAM_ERROR
            return False
        self.end_transaction()
        # Done getting stuff from the transaction.

        # TODO: lock submitting for team.

        # prep match container
        container_path = StorageAPI.prep_match_container(\
            user_team["_id"],target_team["_id"])
        #TODO:  unlock submitting
        # run match
        game_result = GameController.run_game(container_path)
        match_data = game_result[0]
        match_data["defender"] = target_team["name"]
        match_data["submitter"] = username
        match_data["challenger"] = user_team["name"]
        game_id = self.database.logs.insert_one(game_result).inserted_id
        self.ret_val = game_id
        return True
