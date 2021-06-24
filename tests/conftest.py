import pytest
import getpass


def pytest_addoption(parser):
    parser.addoption('--flaskaddr', action='store', default='127.0.0.1:5000', help='IP address and port of flask server. Default is 127.0.0.1:5000')
    parser.addoption('--recvemail', action='store', default=None, help='Email address to receive test emails from.')


@pytest.fixture
def flaskaddr(request):
    temp = request.config.getoption('--flaskaddr')
    return temp

@pytest.fixture
def recvemail(request):
    p = getpass.getpass("\nEmail Password: ")
    email = request.config.getoption('--recvemail')
    return f'{email}:{p}'