import pytest
import requests
import time
import json
import imaplib

from .testbase import BaseTester,  \
    filter_link, \
    read_link,   \
    filter_jwt_token
IMAP_SERVER = 'imap.gmail.com'

# Just a function to be used by a lot of tests


def split(string):
    temp = string.split(':')
    username = temp[0]
    password = temp[1]
    return username, password




# Testing normal login now with the user in the database.
def test_general_login(request, flaskaddr, receive_email):
    email, _ = split(receive_email)
    r = requests.post(f'http://{flaskaddr}/api/user/auth',
                      json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.save_var('JWT_TOKEN_USER', json.loads(r.text)['token'])
        output = filter_jwt_token(r.text)
        test.run(request.node.name, f'{output}HTTP_Status: {r.status_code}')

'''
# Testing creating a new team.
def test_create_team(request, flaskaddr):
    with BaseTester() as test:
        token = test.get_var('JWT_TOKEN_USER').rstrip()
        test.save_var('JWT_TOKEN_USER', token)
        r = requests.post(f'http://{flaskaddr}/api/teams',
                json={'name': 'Battlecode', 'event_id': '612ebdbc35dbeeffdd417559', 'members': ['janice@gmail.com nick@gmail.com']},
                          headers={'Authorization': f'Bearer {token}'})
        test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')
'''
# Getting a team details
def test_get_team(request, flaskaddr):
    with BaseTester() as test:
        token = test.get_var('JWT_TOKEN_USER').rstrip()
        test.save_var('JWT_TOKEN_USER', token)
        r = requests.get(f'http://{flaskaddr}/api/teams',
                         headers={'Authorization': f'Bearer {token}'})
        print(r.status_code)
        print(r.text)
        #test.run(request.node.name, f'HTTP_Status: {r.status_code}')
