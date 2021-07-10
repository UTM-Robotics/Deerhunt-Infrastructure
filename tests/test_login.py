import pytest
import requests
import json

from .testbase import BaseTester, filter_jwt_token

FILTERS = [filter_jwt_token]

def test_login(request, flaskaddr, receive_email):
    temp = receive_email.split(':')
    email = temp[0]
    r = requests.post(f'http://{flaskaddr}/login', json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.save_var('JWT_TOKEN', json.loads(r.text)['token'])
        for filter in FILTERS:
            output = filter(r.text)
        test.run(request.node.name, output)
