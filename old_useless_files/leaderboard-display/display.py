#!/usr/bin/env python3
import pymongo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from sshtunnel import SSHTunnelForwarder

import os
import argparse
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('website_url', help='the url to where the site is being hosted')
parser.add_argument('website_username', help='username to the site')
parser.add_argument('website_password', help='password to the site')
parser.add_argument('--ssh_server', help='the server that your mongo server is running on')
parser.add_argument('--ssh_port', help='the port that your server is running on')
parser.add_argument('--ssh_user', help='the user to log into the server with')
parser.add_argument('--mongo_server', help='the ip that your mongo server is bound to')
parser.add_argument('--mongo_port', help='the port that your mongo server is running on')
args = parser.parse_args()

def default(test, default):
    return default if test is None else test

server = SSHTunnelForwarder(
    (default(args.ssh_server, 'localhost'), default(args.ssh_port, 22)),
    ssh_username = default(args.ssh_user, os.getlogin()),
    remote_bind_address = (default(args.mongo_server, '127.0.0.1'), default(args.mongo_port, 27017))
)

server.start()

client = pymongo.MongoClient('127.0.0.1', server.local_bind_port)
db = client.neodeerhunt

driver = webdriver.Firefox()
driver.get(args.website_url)
driver.find_element_by_id('username').send_keys(args.website_username)
elem = driver.find_element_by_id('password')
elem.send_keys(args.website_password)
elem.send_keys(Keys.RETURN)
sleep(1)
driver.get(str(args.website_url) + '/replay')
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
