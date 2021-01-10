from pymongo import MongoClient
from teams import TeamController
from game_runner import GameController
from storage import StorageAPI
from datetime import datetime
from time import sleep
DATABASE_URL = "mongodb+srv://utmrobotics:1d3erhunted3089@deerhunt.ntpnz.mongodb.net/<dbname>?retryWrites=true&w=majority"
PROD_FLAG = False

class Consumer:
    '''Consumer retrieves matches from the submission queue, runs them and updates the leaderboard '''
    def __init__(self):
        self.client = MongoClient(DATABASE_URL)
        if PROD_FLAG:
            self.database = self.client.deerhunt_prod
        else:
            self.database = self.client.deerhunt_db
        self.session = self.client.start_session()
        self.submission_queue = self.database['submission_queue']
        self.teams = self.database['teams']
        self.challenger = None
        self.defender = None

    def run(self):
        '''run constantly checks to see if there are new submissions, if there is run the match and update the leaderboard'''
        while True:
            #Get the next match and run the match if there is one (by order of modified)
            match = self.submission_queue.find_one(sort=[("modified", 1)])
            if match is not None:
                print("Got match")
                try:
                    self.submission_queue.delete_one({'_id': match['_id']})
                    #Runs the match and gets the result
                    match_string = self.create_match(match)
                    if match_string is not None and not isinstance(match_string, int):
                        print("got match {}".format(match_string))
                        result = GameController.run_game(match_string)
                        self.database.logs.insert_one({"winner": result[1], "data": result[0], "team_id": self.challenger['_id'], "modified": datetime.now()})
                        self.update_leaderboard(result)
                    elif match_string is None:
                        return
                    elif match_string == StorageAPI.P1_ZIP_ERROR: # Handle invalid zip file.
                        print("Got bad match")
                        match_result = {'lines': [],
                            'maps': [],
                            'errors': [],
                            'build_id': []
                            }
                        result = (match_result,1)
                        self.update_leaderboard(result)
                    #Removes the match from the submission queue
                except FileNotFoundError:
                    print("File not found {}".format(self.challenger['_id']))
            else:
                sleep(30)
                
    
    def create_match(self, match: dict) -> str:
        '''create_match creates a new match given the team id's and returns the result '''
        #Gets the 2 players from db object
        self.challenger = self.teams.find_one({"_id": match['challenger_id']})
        self.defender = self.teams.find_one({"_id": match['defender_id']})
        
        #Verifies
        if self.challenger is None or self.defender is None:
            print("Challenger or defender do not exist")
            return

        if self.challenger == self.defender:
            print("Can not challenge own team")
            return

        return StorageAPI.prep_match_container(self.defender['_id'], self.challenger['_id'])

    def update_leaderboard(self, result: tuple):
        '''update_leaderboard gets the results from the recent game and updates the leaderboard according to the results'''
        self.session.start_transaction()
        current_leaderboard = self.database.leaderboard.find_one({'type': 'current'})
        defending_rank, attacking_rank = -1, -1
        print("Updating leaderboard")
        #Gets the defending and challenging team from the leaderboard
        for k,v in enumerate(current_leaderboard["teams"]):
            if v == self.defender['name']:
                defending_rank = k
            if v == self.challenger['name']:
                attacking_rank = k

        print("Got ranks {} and {}".format(defending_rank, attacking_rank))

        #Adds the defender to the bottom of the leaderboard if it is their first submission
        if defending_rank == -1:
            new_leaderboard = current_leaderboard["teams"]
            new_leaderboard.append(self.defender["name"])
            self.database.leaderboard.update_one({"type": "current"}, {"$set" : {"teams": new_leaderboard}})
            current_leaderboard = self.database.leaderboard.find_one({"type" : "current"})

        #If the attacker wins insert them into the defenders spot
        if result[0]['lines'][-1] == 'Winner: p2':
            print("Player 2 won")
            if defending_rank < attacking_rank:
                #moves the attacker in front of defender on the leaderboard
                print("Starting leaderboard {}".format(current_leaderboard["teams"]))
                new_leaderboard = current_leaderboard["teams"]
                if attacking_rank != -1:
                    new_leaderboard.remove(self.challenger['name'])
                new_leaderboard.insert(defending_rank, self.challenger['name'])
                attacking_rank = defending_rank
                print("Updated leaderboard to {}".format(new_leaderboard))
                # self.database.leaderboard.update_one({"_id": current_leaderboard["_id"]}, {"$set": {"teams": []}})
                self.database.leaderboard.update_one({"_id": current_leaderboard["_id"]}, {"$set": {"teams": new_leaderboard}})

        #Adds attacker to bottom if it is its first submission to the leaderboard
        if attacking_rank == -1:
            print("Attacker not on board and lost add to end")
            new_leaderboard = current_leaderboard["teams"]
            new_leaderboard.append(self.challenger['name'])
            self.database.leaderboard.update_one({"type": "current"}, {"$set" : {"teams": new_leaderboard}})
        self.session.commit_transaction()

if __name__ == "__main__":
    consumer = Consumer()
    consumer.run()
