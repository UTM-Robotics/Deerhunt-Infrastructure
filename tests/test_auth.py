import pytest
import requests
import os
import imaplib

from .testbase import BaseTester


IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT   = 993



def test_register(request, flaskaddr):
    testname = request.node.name
    r = requests.post(f'http://{flaskaddr}/register')
    with BaseTester() as test:
        test.run(testname, r.text)


def test_register_email(request, recvemail):
    pass
    # testname = request.node.name
    # mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    # mail.login(TEST_EMAIL, TEST_PASSWD)
    # mail.select('inbox')
    # result, data = mail.search(None, '(FROM utmroboticstesting SUBJECT "Welcome to Deerhunt!")')
    # result, data = mail.fetch('1', '(BODY.PEEK[TEXT])')
    # result, data = mail.fetch('1', '(RFC2822)')
