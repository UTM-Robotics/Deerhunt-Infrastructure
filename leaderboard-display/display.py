import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from sshtunnel import SSHTunnelForwarder

from time import sleep

server = SSHTunnelForwarder(
    ('caesar', 22),
    ssh_username='wolfe',
    remote_bind_address=('127.0.0.1', 27017)
)

server.start()

client = pymongo.MongoClient('127.0.0.1', server.local_bind_port)
db = client.neodeerhunt

driver = webdriver.Firefox()
driver.get('https://deerhunt.utmmcss.com')
driver.find_element_by_id('username').send_keys('jeff')
elem = driver.find_element_by_id('password')
elem.send_keys('jeff')
elem.send_keys(Keys.RETURN)
sleep(1)
driver.get('https://deerhunt.utmmcss.com/replay')
sleep(1)

try:
    while True:
        result = db.leaderboard.find().sort([('time', -1)]).limit(1)[0]
        build = result['takeover_match']
        match = db.logs.find_one({'build_id': build})
        match_id = str(match['_id'])
        print(match_id)
        elem = driver.find_element_by_id('submit')
        elem.send_keys(Keys.CONTROL, 'a')
        elem.send_keys(match_id)
        driver.find_element_by_css_selector('.replay-button').click()
        sleep(1)

        try:
            while True:
                driver.find_element_by_css_selector('#table-body > tr')
                sleep(10)
        except Exception:
            pass

except KeyboardInterrupt:
    print('Exiting...')
finally:
    client.close()
    server.stop()
