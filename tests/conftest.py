import os
import pytest
from dotenv import load_dotenv
from minutemail import Mail

load_dotenv()

# Create a new 10 minute mail session
# to imitate user's email account.
mail = Mail()


# Pytest default function to set default fixtures.
# Enables command line options for fixtures.
def pytest_addoption(parser):
    parser.addoption('--flaskaddr', action='store', default=os.getenv('FLASK_ADDR'), help='IP address and port of flask server. Default is 127.0.0.1:5000')
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
    return mail


# Pytest fixture for default admin creds.
@pytest.fixture
def admin_default_creds(request):
    username = request.config.getoption('--adminusername')
    password = request.config.getoption('--adminpasswd')
    return f'{username}:{password}'
