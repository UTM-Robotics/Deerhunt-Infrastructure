''' Handles all challenge and scrimmage controls.'''

import traceback
from pymongo import MongoClient

from teams import TeamController
from storage import StorageAPI
from game_runner import GameController
from datetime import datetime, timedelta
class ChallengeController:
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

    def can_challenge(self, username, defender_rank, is_scrimmage=False) -> tuple:
        '''Returns whether or not the challenge can be performed by the user to another team.'''
        #Gets users team from database
        team_api = TeamController(self.client, self.database, input_session=self.session)
        user_team = team_api.get_user_team(username)
        if not user_team:
            self.error = self.NOT_ON_TEAM_ERROR
            return None

        #Confirms user hasnt challenged or scrimmaged within 5 minutes
        timer_string = "scrimmage_time" if is_scrimmage else "challenge_time"
        curr_time = datetime.now()
        if timer_string in user_team:
            if curr_time-user_team[timer_string] < timedelta(minutes=5):
                self.error = self.TIMEOUT_ERROR
                return None
        
        #Updates the modified time to now
        time_update_query = {"_id": user_team["_id"]}
        time_update_data = {"$set": {timer_string:curr_time}}
        self.database.teams.update_one(time_update_query,\
            time_update_data, session=self.session)

        #Gets the current leaderboard from database
        current_leaderboard = self.database.leaderboard.find_one({"type": "current"},\
             session=self.session)
        if len(current_leaderboard["teams"]) < defender_rank:
            self.error = self.RANK_OUT_OF_BOUNDS_ERROR
            return None


        #Gets the defending team
        defending_team = team_api.get_team(current_leaderboard["teams"][defender_rank])
        if not defending_team:
            self.error = self.INVALID_TEAM_ERROR
            return None
        if defending_team["_id"] == user_team["_id"]:
            self.error = self.INVALID_TEAM_ERROR
            return None

        #If this is a leaderboard battle make sure the attacker is a lower rank than the defender_rank
        if not is_scrimmage:
            try:
                attacking_rank = current_leaderboard["teams"].index(user_team["name"])
                if attacking_rank < defender_rank:
                    self.error = self.INVALID_TEAM_ERROR
                    return None
            except ValueError:
                pass

        return (user_team, defending_team)

    def queue_challenge(self, username, target_rank):
        '''Adds the team to the challenge queue against team at the target rank'''
        self.start_transaction()
        #Confirms that the user can face the given team
        teams = self.can_challenge(username, target_rank)
        if teams is None:
            return False
        #Adds the teams to the submission queue
        submission = {
            "challenger_id": teams[0]["_id"],
            "defender_id": teams[1]["_id"],
            "modified": datetime.now()
        }
        self.database.submission_queue.insert_one(submission, session=self.session)
        self.end_transaction()

        return True

    def do_scrimmage(self, username, target_rank):
        '''Performs a scrimmage between the user's team and another team at the target rank
            Returns the game_id of the scrimmage.
        '''
        self.start_transaction()
        #Confirms that the user can challenge the given team
        teams = self.can_challenge(username, target_rank, is_scrimmage=True)
        if teams is None:
            return False
        user_team, target_team = teams[0], teams[1]
        self.end_transaction()
        #Prepares the files to run the match
        container_path = StorageAPI.prep_match_container(\
            user_team["_id"],target_team["_id"])
        print("Path:",container_path)
        if isinstance(container_path,int):
            return False
        #Runs the match and returns the results
        game_result = GameController.run_game(container_path)
        game_save = self.database.logs.insert_one({"winner": game_result[1],\
             "data": game_result[0], "team_id": user_team["_id"],"modified": datetime.now()})
        self.ret_val = game_save.inserted_id
        return True
