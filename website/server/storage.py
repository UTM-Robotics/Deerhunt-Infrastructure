""" Helpers for all local machine's storage-related actions."""

import os
import uuid
import shutil
from zipfile import ZipFile, BadZipFile

class StorageAPI:
    ''' Class for all storage-related actions'''
    PREFIX = '/deerhunt'
    SUBMISSIONS_FOLDER = f'{PREFIX}/submissions'
    BUILD_FOLDER = f'{PREFIX}/build'
    TEMPLATE_FOLDER = f'{PREFIX}/template'
    SERVER_FOLDER = f'{PREFIX}/server'

    @staticmethod
    def save(file, team_id):
        ''' Saves the file using the team name'''
        file_path = f'{StorageAPI.SUBMISSIONS_FOLDER}/{team_id}'
        file.save(f'{StorageAPI.SUBMISSIONS_FOLDER}/{team_id}.zip')
        try:
            with ZipFile(f'{file_path}.zip', 'r') as z:
                z.extractall(file_path)
        except BadZipFile:
            return False
        os.remove(f'{file_path}.zip')
        return True

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
        StorageAPI.copy_dir_contents(f'{StorageAPI.SUBMISSIONS_FOLDER}/{p1_team_id}',\
             f'{build_path}/p1')
        StorageAPI.copy_dir_contents(f'{StorageAPI.SUBMISSIONS_FOLDER}/{p2_team_id}',\
             f'{build_path}/p2')
        return build_path

    @staticmethod
    def copy_dir_contents(src, dest):
        ''' Copies the contents of a directory into another directory.'''
        for file in os.listdir(src):
            shutil.copy(f'{src}/{file}', dest)
