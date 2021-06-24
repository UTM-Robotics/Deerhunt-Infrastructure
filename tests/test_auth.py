import pytest
import requests
import os
import imaplib

from .testbase import BaseTester, filter_code



FILTERS = [filter_code]

IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT   = 993



# The initial postrequest to server to register.
def test_register(request, flaskaddr):
    r = requests.post(f'http://{flaskaddr}/register', json={'email': 'utmroboticstestingrecv@gmail.com'})
    with BaseTester() as test:
        test.run(request.node.name, r.text)


# Opening test gmail acount and downloading 
# new email that should havbe been received.
def test_register_email(request, recvemail):
    temp = recvemail.split(':')
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
        for filter in FILTERS:
            output = filter(body)
        test.run(request.node.name, output)
