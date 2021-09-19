import pytest
import requests
import imaplib
import time
import json

from .testbase import   BaseTester,  \
                        filter_link, \
                        read_link,   \
                        filter_jwt_token
IMAP_SERVER = 'imap.gmail.com'




# This function assumes the user doesn't exist in mongodb.
# Error checking to make sure login error handles correctly.
def test_general_login_non_existing(request, flaskaddr, receive_email):
    email = str(receive_email)
    r = requests.post(f'http://{flaskaddr}/api/login', json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')


# The initial post request to server to register.
# This function assumes the user doesn't exist in mongodb.
def test_register(request, flaskaddr, receive_email):
    email = str(receive_email)
    r = requests.post(f'http://{flaskaddr}/api/register', 
                    json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')


# Opening test gmail acount and downloading 
# new email that should havbe been received.
def test_register_email(request, receive_email):
    while True:
        if receive_email.new_message():  # Check for new mail
            body = receive_email.fetch_message()[0]['bodyHtmlContent']  # Fetch all the messages
            break
        time.sleep(2)
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
    email = str(receive_email)
    r = requests.post(f'http://{flaskaddr}/api/register', 
                    json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')


# Testing normal login now with the user in the database.
def test_general_login(request, flaskaddr, receive_email):
    email = str(receive_email)
    r = requests.post(f'http://{flaskaddr}/api/login', json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.save_var('JWT_TOKEN_USER', json.loads(r.text)['token'])
        output = filter_jwt_token(r.text)
        test.run(request.node.name, f'{output}HTTP_Status: {r.status_code}')


# Testing admin login with incorrect password
def test_admin_login_error(request, flaskaddr):
    r = requests.post(f'http://{flaskaddr}/api/adminlogin', json={'username': 'nonexistent', 'password': 'tester1234'})
    with BaseTester() as test:
        output = filter_jwt_token(r.text)
        test.run(request.node.name, f'{output}HTTP_Status: {r.status_code}')


# Testing to make sure default admin login works.
def test_admin_login(request, flaskaddr, admin_default_creds):
    temp = admin_default_creds.split(':')
    username = temp[0]
    password = temp[1]
    r = requests.post(f'http://{flaskaddr}/api/adminlogin', json={'username': username, 'password': password})
    with BaseTester() as test:
        output = filter_jwt_token(r.text)
        test.run(request.node.name, f'{output}HTTP_Status: {r.status_code}')

def test_teardown(request, flaskaddr, receive_email):
    email = str(receive_email)
    with BaseTester() as test:
        token = test.get_var('JWT_TOKEN_USER').rstrip()
        r = requests.delete(f'http://{flaskaddr}/api/login', 
                            json={'email': email},
                            headers={'Authorization': f'Bearer {token}'})
        test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')
