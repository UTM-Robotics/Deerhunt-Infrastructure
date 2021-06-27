import pytest
import requests
import imaplib
import time

from .testbase import BaseTester, filter_link, read_link



FILTERS = [filter_link]

IMAP_SERVER = 'imap.gmail.com'
# IMAP_PORT   = 993


# The initial postrequest to server to register.
def test_register(request, flaskaddr, recvemail):
    temp = recvemail.split(':')
    email = temp[0]
    r = requests.post(f'http://{flaskaddr}/register', json={'email': email, 'password': 'tester1234'})
    with BaseTester() as test:
        test.run(request.node.name, r.text)


# Opening test gmail acount and downloading 
# new email that should havbe been received.
def test_register_email(request, recvemail):
    time.sleep(5)
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
    # VERIFY_LINK = re.search(EMAIL_URL_REGEX, body).group(1)
    # read_link(body)
    with BaseTester() as test:
        test.save_var('VERIFY_LINK', read_link(body))
        for filter in FILTERS:
            output = filter(body)
        test.run(request.node.name, output)

def test_verify_link(request):
    with BaseTester() as test:
        link = test.get_var('VERIFY_LINK')
        r = requests.post(link)
        test.run(request.node.name, r.text)