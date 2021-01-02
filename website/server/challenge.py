''' Handles all challenge and scrimmage controls.'''

import traceback
from pymongo import MongoClient


class ChallengeController:
    ''' Performs all Teams-related logic with Database.'''

    # ChallengeController Errors

    def __init__(self, client: MongoClient, database):
        self.client = client
        self.database = database
        self.session = self.client.start_session()
        self.error = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.session.end_session()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False
        return True

    def start_transaction(self):
        ''' Starts the transaction for an object with an activated session'''
        self.session.start_transaction()

    def end_transaction(self):
        ''' Ends the transaction for an object with an activated session'''
        self.session.commit_transaction()

    def can_challenge(self, user, target_rank):
        '''Returns whether or not the challenge can be performed by the user to another team.'''
        pass

    def queue_challenge(self, team, target_rank):
        '''Adds the team to the challenge queue against team at the target rank'''
        # get user team
        # add team to challenge queue.

    def do_scrimmage(self, user, target_rank):
        '''Performs a scrimmage between the user's team and another team at the target rank
            Returns the game_id of the scrimmage.
        '''
        # get user team
        # get team at target rank
        # lock submitting for team.
        # prep match container
        # unlock submitting
        # run match
        # log match , use tag *scrimmage*
        # set output to winner.
