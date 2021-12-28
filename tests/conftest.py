import os
import pytest
from dotenv import load_dotenv

load_dotenv()

'''
Pytest default function to set default fixtures.
Enables command line options for fixtures.

You can pass in parameters using the .env file or just using command line parameters listed below.
eg:
$ pytest --flaskaddr 192.168.0.231:8000
$ pytest --recvemail testing@gmail.com --passwd abcd1234 --adminusername admin --adminpasswd admin
'''
def pytest_addoption(parser):
    parser.addoption('--flaskaddr', action='store', default=os.getenv('FLASK_ADDR'), help='IP address and port of flask server. Default is 127.0.0.1:5000')
    parser.addoption('--recvemail', action='store', default=os.getenv('TEST_EMAIL_ADDR'), help='Email address to receive test emails from.')
    parser.addoption('--passwd', action='store', default=os.getenv('TEST_EMAIL_PASSWD'), help='Password for email.')
    parser.addoption('--adminusername', action='store', default=os.getenv('ADMIN_USERNAME'), help='Default admin account username')
    parser.addoption('--adminpasswd', action='store', default=os.getenv('ADMIN_PASSWORD'), help='Default admin account password')


# Pytest fixture for address of flask server and port.
@pytest.fixture
def flaskaddr(request):
    return request.config.getoption('--flaskaddr')


# Pytest fixture for 10minutemail object.
# Used by some test functions to register, read email etc.
@pytest.fixture
def receive_email(request):
    password = request.config.getoption('--passwd')
    email = request.config.getoption('--recvemail')
    return f'{email}:{password}'


# Pytest fixture for default admin creds.
@pytest.fixture
def admin_default_creds(request):
    username = request.config.getoption('--adminusername')
    password = request.config.getoption('--adminpasswd')
    return f'{username}:{password}'
