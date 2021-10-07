import pytest
import requests
import time
import json

from .testbase import   BaseTester,  \
                        filter_link, \
                        read_link,   \
                        filter_jwt_token, \
                        read_jwt_token


# The initial post request to server to register.
# This function assumes the user doesn't exist in mongodb.
def test_register(request, flaskaddr, receive_email):
    email = str(receive_email)
    print(email)
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

# Testing normal login now with the user in the database.
def test_general_login(request, flaskaddr, receive_email):
    email = str(receive_email)
    r = requests.post(f'http://{flaskaddr}/api/login', json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.save_var('JWT_TOKEN_USER', json.loads(r.text)['token'])
        output = filter_jwt_token(r.text)
        test.run(request.node.name, f'{output}HTTP_Status: {r.status_code}')


def test_create_team(request, flaskaddr):
    with BaseTester() as test:
        jwt_token = test.get_var('JWT_TOKEN_USER').rstrip()
        print(repr(jwt_token))
        r = requests.post(f'http://{flaskaddr}/api/teams',
                            json={'name': 'pied piper'},
                            headers={'Authorization': f'Bearer {jwt_token}'})
        print(r.text)
        