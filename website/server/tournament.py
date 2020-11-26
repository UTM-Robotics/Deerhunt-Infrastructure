#!/usr/bin/python
import random

class TournamentLevel:

    def __init__(self, submissions: dict):
        self.init_teams_dict = submissions


    def run(self):
        '''
        Runs tournament battles until there is one top winner.
        '''
        self.all = TournamentLevel.shuffle(self.init_teams_dict)
        while len(self.all[0]) > 1:
            print(self.all)
            self.all = TournamentLevel.runTournament(self.all)


    @staticmethod
    def shuffle(submissions):
        '''
        This wrapper shuffles and rearranges list of dictionaries to be in the form [ [{}, {}] ]
        Each dictionary represents a single team and their submission path.
        '''
        retList = list()
        for i in submissions:
            temp = {}
            temp[i] = submissions[i]
            retList.append(temp)
        print("original: ", retList)
        random.shuffle(retList)
        print("list after shuffle ", retList)
        return list(retList)

    @staticmethod
    def runTournament(rootList: list):
        '''
        Runs entire tournament simulation.
        Returns a single list
        '''
        num_of_brackets = len(rootList)
        retList = list()
        for k in range(num_of_brackets):
            retList.append(list())
        retList.append(list())

        for bracket in range(num_of_brackets):
            num_of_teams = len(rootList[bracket])
            for teams in range(num_of_teams // 2):
                player1 = rootList[bracket][teams]
                player2 = rootList[bracket][-1*(teams+1)]
                result = battle(player1, player2) # STILL NEEDS TO BE WRITTEN
                if result == 0:
                    retList[bracket].append(player1)
                    retList[bracket+1].append(player2)
                elif result == 1:
                    retList[bracket].append(player2)
                    retList[bracket].append(player1)
            if num_of_teams % 2 != 0:
                retList[bracket].append(rootList[bracket][num_of_teams // 2]) # Might have to update num of wins per team.
        return retList

    @staticmethod
    def battle(player1: dict, player2: dict):
        '''
        Returns 0 if player1 wins.
        Returns 1 if player2 wins. 
        '''
        print(player1)
        print(player2)
        return random.randint(0,10) % 2