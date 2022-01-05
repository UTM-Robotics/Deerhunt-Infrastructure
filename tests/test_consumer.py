import pytest
import requests
import json

from .testbase import BaseTester,  \
    filter_link, \
    read_link,   \
    filter_jwt_token


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
def test_challenge(request, flaskaddr):
    #email, _ = split(receive_email)
    with BaseTester() as test:
        token = test.get_var('JWT_TOKEN_USER').rstrip()
        r = requests.post(f'http://{flaskaddr}/api/requests',
                json={'name': 'Battlecode', 'team1_id': '61d53a19dfd074d4783b18ac',                       'team2_id':'61d5401b732eca2411190bed'},
                            headers={'Authorization': f'Bearer {token}'})
        print(r.text)

'''
def test_consume_match(request, flaskaddr, receive_email):
    r = requests.get(f'http://{flaskaddr}/api/requests',
                    json={'event_id': '61d5387adfd074d4783aa8ad', 'token': 'blabla'})
    print(r.text)
'''
