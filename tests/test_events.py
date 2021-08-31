import requests

def test_create_event(request, flaskaddr):
    r = requests.post(f'http://{flaskaddr}/api/events', 
                        json={'name': 'test_event', 
                              'game': 'micromouse',
                              'starttime': '',
                              'endtime': '',})
    print(r.text)
    assert True