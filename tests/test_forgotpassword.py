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

# simulates a user clicking forgot password, entering the email
# they registered with and submitting.
def test_forgotpassword_init(request, flaskaddr, receive_email):
    email, _ = split(receive_email)
    r = requests.post(f'http://{flaskaddr}/api/user/forgotpassword', 
                json={'email': email})
