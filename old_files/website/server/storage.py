""" Helpers for all local machine's storage-related actions."""

import os
import uuid
import shutil
import traceback
import datetime
from pymongo import MongoClient
from zipfile import ZipFile, BadZipFile


class StorageAPI:
    FAILED_UPDATE_SUBMIT_TIME = 1
    FAILED_NEED_MORE_TIME = 2
    FAILED_EMPTY_FILE = 3

    ''' Class for all storage-related actions'''
    PREFIX = '/deerhunt'
    SUBMISSIONS_FOLDER = f'{PREFIX}/submissions'
    BUILD_FOLDER = f'{PREFIX}/build'
    TEMPLATE_FOLDER = f'{PREFIX}/template'
    SERVER_FOLDER = f'{PREFIX}/server'
    # Errors
    P1_ZIP_ERROR = 1
    P2_ZIP_ERROR = 2

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

    def save(self, uploaded_file, team_obj_id):
        print(uploaded_file.filename)
        print(uploaded_file)
        if uploaded_file.filename == '':
            self.abort_transaction(self.FAILED_EMPTY_FILE)
        self.start_transaction()
        team_id = str(team_obj_id)
        team_file = self.database.teams.find_one({"_id": team_obj_id}, session=self.session)
        if "last_submitted" not in team_file:
            # Team is submitting for the first time.
            result = self.database.teams.update_one({"_id": team_obj_id}, {"$set": {"last_submitted": datetime.datetime.now()}}, session=self.session)
            if result.modified_count != 1:
                self.abort_transaction(self.FAILED_UPDATE_SUBMIT_TIME)
                return False
        else:
            # not first time, check if 5 minute have passed
            last_submitted = team_file["last_submitted"] # this should be a datetime.datetime object
            current_time = datetime.datetime.now()
            print("Attempting submission for team: ",team_file["name"])
            print("last_submitted: " + str(last_submitted))
            print( "delta: ", last_submitted + datetime.timedelta(minutes=1))
            print("current_time: " + str(current_time))
            if (last_submitted + datetime.timedelta(minutes=5) ) < current_time and False:
                # not enough time has passed
                print("5 MINUTES NOT PASSED YET!")
                self.abort_transaction(self.FAILED_NEED_MORE_TIME)
                return False
            else:
                result = self.database.teams.update_one({"_id": team_obj_id}, {"$set": {"last_submitted": datetime.datetime.now()}}, session=self.session)
                if result.modified_count != 1:
                    self.abort_transaction(self.FAILED_UPDATE_SUBMIT_TIME)
                    return False
        
        ''' Saves the file using the team name'''
        file_path = f'{self.SUBMISSIONS_FOLDER}/{team_id}'
        uploaded_file.save(f'{file_path}.zip')
        self.commit_transaction()
        return True

    def start_transaction(self):
        self.session.start_transaction()

    def commit_transaction(self):
        self.session.commit_transaction()

    def abort_transaction(self, error_num):
        self.error = error_num
        self.session.abort_transaction()



    @staticmethod
    def prep_match_container(p1_team_id, p2_team_id):
        ''' Returns the path to a container prepped for a match.
            Preps a match container to be run with p1_team and p2_team.
        '''
        uid = uuid.uuid4().hex
        # Unique build folder for this match.
        build_path = f'{StorageAPI.BUILD_FOLDER}/{uid}'

        shutil.copytree(StorageAPI.TEMPLATE_FOLDER, f'{build_path}/')
        shutil.copytree(StorageAPI.SERVER_FOLDER, f'{build_path}/server')
        if not StorageAPI.copy_zip_contents(f'{StorageAPI.SUBMISSIONS_FOLDER}/{p2_team_id}',
                                            f'{build_path}/p2'):
            return StorageAPI.P2_ZIP_ERROR
        if not StorageAPI.copy_zip_contents(f'{StorageAPI.SUBMISSIONS_FOLDER}/{p1_team_id}',
                                            f'{build_path}/p1'):
            return StorageAPI.P1_ZIP_ERROR
        return build_path

    '''
    @staticmethod
    def is_zip(file_path):
        try: 
            return ZipFile.is_zipfile(f'{file_path}.zip')
        except Exception as e:
            return False
    '''

    @staticmethod
    def copy_zip_contents(src, dest):
        ''' Copies the contents of a directory into another directory.'''
        try:
            with ZipFile(f'{src}.zip', 'r') as zip_file:
                zip_file.extractall(dest)
                return True
        except BadZipFile:
            return False
