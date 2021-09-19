import requests
from .testbase import   BaseTester,  \
                        filter_link, \
                        read_link,   \
                        filter_jwt_token


def test_create_event(request, flaskaddr):
    r = requests.post(f'http://{flaskaddr}/api/events', 
                        json={'name': 'test_event2', 
                              'game': 'micromouse',
                              'starttime': '',
                              'endtime': '',})
    # with BaseTester() as test:
        # test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')


def test_get_all_events(request, flaskaddr):
    r = requests.get(f'http://{flaskaddr}/api/events')
    print(r.text)
    # with BaseTester() as test:
        # test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')


def test_delete_event(request, flaskaddr):
    r = requests.delete(f'http://{flaskaddr}/api/events')
    print(r.text)
    # with BaseTester() as test:
        # test.run(request.node.name, f'{r.text}HTTP_Status: {r.status_code}')
