import os
import pytest
from dotenv import load_dotenv

load_dotenv()


def pytest_addoption(parser):
    parser.addoption('--flaskaddr', action='store', default=os.getenv('FLASK_ADDR'), help='IP address and port of flask server. Default is 127.0.0.1:5000')
    parser.addoption('--recvemail', action='store', default=os.getenv('TEST_EMAIL'), help='Email address to receive test emails from.')
    parser.addoption('--passwd', action='store', default=os.getenv('TEST_PASSWD'), help='Password for email.')



@pytest.fixture
def flaskaddr(request):
    return request.config.getoption('--flaskaddr')

@pytest.fixture
def recvemail(request):
    p = request.config.getoption('--passwd')
    email = request.config.getoption('--recvemail')
    return f'{email}:{p}'
