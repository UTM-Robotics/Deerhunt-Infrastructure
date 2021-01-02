from pymongo import MongoClient
from match import Match

DATABASE_URL = "mongodb+srv://utmrobotics:1d3erhunted3089@deerhunt.ntpnz.mongodb.net/<dbname>?retryWrites=true&w=majority"
PROD_FLAG = False

class Consumer:
    def __init__(self):
        #Connects to the correct database
        client = MongoClient(DATABASE_URL)
        if PROD_FLAG:
            #self.database = client.deerhunt_prod
            raise NotImplementedError()
        else:
            self.database = client.deerhunt_db

        #Get the required columns from the database
        self.submission_queue = self.database["submission_queue"]
        self.leaderboards = self.database["leaderboard"]
        self.teams = self.database["teams"]

    #run constantly checks the datbase for new submission_queue to be run
    def run(self):
        while True:
            #Get the next match and run the match if there is one (by order of modified)
            match = self.submission_queue.find_one(sort=[("modified", 1)])
            if match is not None:
                print("There is a match!")
                #Gets the 2 players from db object
                challenger = self.teams.find_one({"_id": match['challenger_id']})
                defender = self.teams.find_one({"_id": match['defender_id']})
                print(type(challenger))

                #Creates, runs and displays result of a new match
                new_match = Match(challenger, defender)
                new_match.runMatch()
                print(new_match.result)
                #Removes the match from the submission queue
                #self.submission_queue.delete_one({'_id': match['_id']})
                break