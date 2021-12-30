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


# The initial post request to server to register.
# This function assumes the user doesn't exist in mongodb.
def test_register(request, flaskaddr, receive_email):
    email, _ = split(receive_email)
    r = requests.post(f'http://{flaskaddr}/api/user',
                      json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')


# Opening test gmail acount and downloading
# new email that should havbe been received.
def test_register_email(request, receive_email):
    time.sleep(3)
    email, passwd = split(receive_email)
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(email, passwd)
    mail.select('inbox')
    _, data = mail.search(
        None, '(FROM utmroboticstesting SUBJECT "Welcome to Deerhunt!")')
    msg = data[0].decode('utf-8').split(' ')[-1]
    _, data = mail.fetch(msg, '(BODY.PEEK[TEXT])')
    body = data[0][1].decode('utf-8')
    with BaseTester() as test:
        test.save_var('VERIFY_LINK', read_link(body))
        output = filter_link(body)
        test.run(request.node.name, output)


# Sends the get request to the link received in the email.
# Simulates a user opening their email and clicking the very link.
def test_verify_link(request):
    with BaseTester() as test:
        link = test.get_var('VERIFY_LINK')
        r = requests.get(link)
        output = filter_jwt_token(r.text)
        test.run(request.node.name, f'{output}HTTP_Status: {r.status_code}')


# Testing normal login now with the user in the database.
def test_general_login(request, flaskaddr, receive_email):
    email, _ = split(receive_email)
    r = requests.post(f'http://{flaskaddr}/api/user/auth',
                      json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.save_var('JWT_TOKEN_USER', json.loads(r.text)['token'])
        output = filter_jwt_token(r.text)
        test.run(request.node.name, f'{output}HTTP_Status: {r.status_code}')


# Testing creating a new team.
def test_create_team(request, flaskaddr):
    with BaseTester() as test:
        token = test.get_var('JWT_TOKEN_USER').rstrip()
        test.save_var('JWT_TOKEN_USER', token)
        r = requests.post(f'http://{flaskaddr}/api/teams',
                          json={'name': 'test_team'},
                          headers={'Authorization': f'Bearer {token}'})
        test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')


# Getting a team details
def test_get_team(request, flaskaddr):
    with BaseTester() as test:
        token = test.get_var('JWT_TOKEN_USER').rstrip()
        test.save_var('JWT_TOKEN_USER', token)
        r = requests.get(f'http://{flaskaddr}/api/teams?name=test_team',
                         headers={'Authorization': f'Bearer {token}'})
        test.run(request.node.name, f'HTTP_Status: {r.status_code}')

# Updating a team.
def test_update_team(request, flaskaddr):
    with BaseTester() as test:
        token = test.get_var('JWT_TOKEN_USER').rstrip()
        test.save_var('JWT_TOKEN_USER', token)
        r = requests.put(f'http://{flaskaddr}/api/teams',
                            json={'name': 'test_team', 'eventID': "1234"},
                            headers={'Authorization': f'Bearer {token}'})
        test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')


# Deleting a team.
def test_delete_team(request, flaskaddr):
    with BaseTester() as test:
        token = test.get_var('JWT_TOKEN_USER').rstrip()
        test.save_var('JWT_TOKEN_USER', token)
        r = requests.delete(f'http://{flaskaddr}/api/teams',
                            json={'name': 'test_team'},
                            headers={'Authorization': f'Bearer {token}'})
        test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')


# Running delete user.
def test_teardown(request, flaskaddr, receive_email):
    email, _ = split(receive_email)
    with BaseTester() as test:
        token = test.get_var('JWT_TOKEN_USER').rstrip()
        r = requests.delete(f'http://{flaskaddr}/api/user/auth',
                            json={'email': email},
                            headers={'Authorization': f'Bearer {token}'})
        test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')
