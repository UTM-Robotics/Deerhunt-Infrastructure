'''server/app.py - main api app declaration'''
from flask import Flask, jsonify, send_from_directory, request, abort, session
from flask_cors import CORS
from pymongo import MongoClient
from passlib.hash import sha512_crypt

'''Main wrapper for app creation'''
app = Flask(__name__, static_folder='../build')
app.secret_key = b'a*\xfac\xd4\x940 m\xcf[\x90\x7f*P\xac\xcdk{\x9e3)e\xd7q\xd1n/>\xec\xec\xe0'
CORS(app)

database = MongoClient('localhost', 27017).neodeerhunt

##
# API routes
##

@app.route('/api/login', methods=['POST'])
def login():
    u, p = safe_get_user_and_pass()

    result = database.users.find_one({'username': u})
    if result is None or 'password' not in result:
        abort(403)

    if not sha512_crypt.verify(p, result['password']):
        abort(403)
    
    session['logged_in'] = True
    session['username'] = u

    return 'Login successful'
    

@app.route('/api/register', methods=['POST'])
def register():
    u, p = safe_get_user_and_pass()

    result = database.users.find_one({'username': u})
    if result is not None:
        abort(409)

    database.users.insert_one({'username': u,
                               'password': sha512_crypt.encrypt(p)})

    return 'Register successful'


##
# View route
##

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  '''Return index.html for all non-api routes'''
  #pylint: disable=unused-argument
  return send_from_directory(app.static_folder, 'index.html')

##
# Helpers
##

def safe_get_user_and_pass():
    if not request.is_json:
        abort(400)

    body = request.get_json()

    return body['username'], body['password']
