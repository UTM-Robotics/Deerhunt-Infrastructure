import pytest
import requests
import json

from .testbase import BaseTester, filter_jwt_token

FILTERS = [filter_jwt_token]

def test_general_login(request, flaskaddr, receive_email):
    temp = receive_email.split(':')
    email = temp[0]
    r = requests.post(f'http://{flaskaddr}/api/login', json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.save_var('JWT_TOKEN', json.loads(r.text)['token'])
        output = filter_jwt_token(r.text)
        test.run(request.node.name, output)


def test_admin_login(request, flaskaddr, admin_default_creds):
    temp = admin_default_creds.split(':')
    username = temp[0]
    password = temp[1]
    r = requests.post(f'http://{flaskaddr}/api/admin', json={'username': username, 'password': password})
    with BaseTester() as test:
        test.save_var('JWT_TOKEN', json.loads(r.text)['token'])
        output = filter_jwt_token(r.text)
        test.run(request.node.name, output)
