import os
import pytest
from dotenv import load_dotenv

load_dotenv()


def pytest_addoption(parser):
    parser.addoption('--flaskaddr', action='store', default=os.getenv('FLASK_ADDR'), help='IP address and port of flask server. Default is 127.0.0.1:5000')
    parser.addoption('--recvemail', action='store', default=os.getenv('TEST_EMAIL'), help='Email address to receive test emails from.')
    parser.addoption('--passwd', action='store', default=os.getenv('TEST_PASSWD'), help='Password for email.')
    parser.addoption('--adminusername', action='store', default=os.getenv('ADMIN_USERNAME'), help='Default admin account username')
    parser.addoption('--adminpasswd', action='store', default=os.getenv('ADMIN_PASSWORD'), help='Default admin account password')



@pytest.fixture
def flaskaddr(request):
    return request.config.getoption('--flaskaddr')

@pytest.fixture
def receive_email(request):
    password = request.config.getoption('--passwd')
    email = request.config.getoption('--recvemail')
    return f'{email}:{password}'

@pytest.fixture
def admin_default_creds(request):
    username = request.config.getoption('--adminusername')
    password = request.config.getoption('--adminpasswd')
    return f'{username}:{password}'
