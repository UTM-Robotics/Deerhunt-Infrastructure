import requests
import json
from .testbase import   BaseTester,  \
                        filter_link, \
                        read_link,   \
                        filter_jwt_token


# Just a function to be used by a lot of tests
def split(string):
    temp = string.split(':')
    username = temp[0]
    password = temp[1]
    return username, password

# Testing to make sure default admin login works.
def test_admin_login(request, flaskaddr, admin_default_creds):
    username, password = split(admin_default_creds)
    r = requests.post(f'http://{flaskaddr}/api/admin/auth', json={'username': username, 'password': password})
    with BaseTester() as test:
        test.save_var('JWT_TOKEN_ADMIN', json.loads(r.text)['token'])
        output = filter_jwt_token(r.text)
        test.run(request.node.name, f'{output}HTTP_Status: {r.status_code}')

def test_create_event(request, flaskaddr):
    with BaseTester() as test:
        token = test.get_var('JWT_TOKEN_ADMIN').rstrip()
        r = requests.post(f'http://{flaskaddr}/api/events', 
                        json={'name': 'Showdown 2', 
                              'game': 'Battlecode',
                              'starttime': '',
                              'endtime': '',},
                        headers={'Authorization': f'Bearer {token}'})
    print(r.text)

def test_get_all_events(request, flaskaddr):
    r = requests.get(f'http://{flaskaddr}/api/events')
    print('\n'+r.text)
    # with BaseTester() as test:
        # test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')

'''
def test_delete_event(request, flaskaddr):
    r = requests.delete(f'http://{flaskaddr}/api/events')
    print(r.text)
    # with BaseTester() as test:
        # test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')
'''
