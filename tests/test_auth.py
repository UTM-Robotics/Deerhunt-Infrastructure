import pytest
import requests
import imaplib
import time
import json

from .testbase import   BaseTester,  \
                        filter_link, \
                        read_link,   \
                        filter_jwt_token



# FILTERS = [filter_link, filter_jwt_token]

IMAP_SERVER = 'imap.gmail.com'
# IMAP_PORT   = 993


# The initial postrequest to server to register.
def test_register(request, flaskaddr, receive_email):
    temp = receive_email.split(':')
    email = temp[0]
    r = requests.post(f'http://{flaskaddr}/register', json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.run(request.node.name, r.text)


# Opening test gmail acount and downloading 
# new email that should havbe been received.
def test_register_email(request, receive_email):
    time.sleep(3)
    temp = receive_email.split(':')
    email = temp[0]
    passwd = temp[1]
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


def test_verify_link(request):
    with BaseTester() as test:
        link = test.get_var('VERIFY_LINK')
        r = requests.get(link)
        test.save_var('JWT_TOKEN', json.loads(r.text)['token'])
        output = filter_jwt_token(r.text)
        test.run(request.node.name, output)
