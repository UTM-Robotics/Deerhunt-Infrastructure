import pytest
import requests
import time
import json
import imaplib

from .testbase import   BaseTester,  \
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


# This function assumes the user doesn't exist in mongodb.
# Error checking to make sure login error handles correctly.
def test_general_login_non_existing(request, flaskaddr, receive_email):
    email, _ = split(receive_email)
    r = requests.post(f'http://{flaskaddr}/api/user/auth', json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')


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
    _, data = mail.search(None, '(FROM utmroboticstesting SUBJECT "Welcome to Deerhunt!")')
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


# Make a request to flask server simulating user 
# creating an account that already exists.
# Checking if error handling is correct.
def test_register_existing_user(request, flaskaddr, receive_email):
    email, _ = split(receive_email)
    r = requests.post(f'http://{flaskaddr}/api/user', 
                    json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')


# Testing normal login now with the user in the database.
def test_general_login(request, flaskaddr, receive_email):
    email, _ = split(receive_email)
    r = requests.post(f'http://{flaskaddr}/api/user/auth', json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.save_var('JWT_TOKEN_USER', json.loads(r.text)['token'])
        output = filter_jwt_token(r.text)
        test.run(request.node.name, f'{output}HTTP_Status: {r.status_code}')


# Testing admin login with incorrect password
def test_admin_login_error(request, flaskaddr):
    r = requests.post(f'http://{flaskaddr}/api/admin/auth', json={'username': 'nonexistent', 'password': 'tester1234'})
    with BaseTester() as test:
        output = filter_jwt_token(r.text)
        test.run(request.node.name, f'{output}HTTP_Status: {r.status_code}')


# Testing to make sure default admin login works.
def test_admin_login(request, flaskaddr, admin_default_creds):
    username, password = split(admin_default_creds)
    r = requests.post(f'http://{flaskaddr}/api/admin/auth', json={'username': username, 'password': password})
    with BaseTester() as test:
        test.save_var('JWT_TOKEN_ADMIN', json.loads(r.text)['token'])
        output = filter_jwt_token(r.text)
        test.run(request.node.name, f'{output}HTTP_Status: {r.status_code}')


# Testing creating a new event as admin.
def test_create_event(request, flaskaddr):
    with BaseTester() as test:
        token = test.get_var('JWT_TOKEN_ADMIN').rstrip()
        test.save_var('JWT_TOKEN_ADMIN', token)
        r = requests.post(f'http://{flaskaddr}/api/events', 
                            json={'name': 'test_event3', 
                                'game': 'micromouse',
                                'starttime': '',
                                'endtime': '',},
                            headers={'Authorization': f'Bearer {token}'})
        test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')


# Getting a list of all scheduled events
def test_get_all_events(request, flaskaddr):
    r = requests.get(f'http://{flaskaddr}/api/events')
    with BaseTester() as test:
        test.run(request.node.name, f'HTTP_Status: {r.status_code}')


# Deleting an event.
def test_delete_event(request, flaskaddr):
    with BaseTester() as test:
        token = test.get_var('JWT_TOKEN_ADMIN').rstrip()
        r = requests.delete(f'http://{flaskaddr}/api/events',
                            json={'name': 'test_event3'},
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
