#!/usr/bin/python
import sys
import json

class Tournament():

    def __init__(self, submissions):
        self.allTeams = submissions


dictionary = json.loads(sys.argv[1])