import pytest
import requests
import os
import imaplib

from .testbase import BaseTester

TEST_EMAIL   = 'UTMRoboticsTestingRecv@gmail.com'
TEST_PASSWD    = 'ptPXDCVRcMh3Gif'
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT   = 993


def test_register(request):
    testname = request.node.name
    r = requests.post('http://127.0.0.1:5000/register', json = {'email': 'UTMRoboticsTestingRecv@gmail.com', 'password': 'ptPXDCVRcMh3Gif'})
    with BaseTester() as test:
        test.run(testname, r.text)


def test_register_email(request):
    testname = request.node.name
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(TEST_EMAIL, TEST_PASSWD)
    mail.select('inbox')
    # result, data = mail.search(None, '(FROM utmroboticstesting SUBJECT "Welcome to Deerhunt!")')
    result, data = mail.fetch('1', '(BODY.PEEK[TEXT])')
    # result, data = mail.fetch('1', '(RFC2822)')
    # Get email contents and match against ref.
    