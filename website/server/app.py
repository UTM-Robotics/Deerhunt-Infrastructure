'''server/app.py - main api app declaration'''
from flask import Flask, jsonify, send_from_directory, request, abort, session
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from passlib.hash import sha512_crypt
from zipfile import ZipFile
from leaderboard import Leaderboard
import uuid
import docker
import time
import shutil
import os

'''Main wrapper for app creation'''
app = Flask(__name__, static_folder='../build')
app.secret_key = b'a*\xfac\xd4\x940 m\xcf[\x90\x7f*P\xac\xcdk{\x9e3)e\xd7q\xd1n/>\xec\xec\xe0'
CORS(app)

board = Leaderboard()
database = MongoClient('localhost', 27017).neodeerhunt
dock= docker.from_env()

prefix = '/deerhunt'
submissions_folder = f'{prefix}/submissions'
build_folder = f'{prefix}/build'
template_folder = f'{prefix}/template'
server_folder = f'{prefix}/server'

##
# API routes
##

@app.route('/api/submit', methods=['POST'])
def submit():
    login_guard()

    if 'upload' not in request.files or 'position' not in request.form:
        abort(400)

    try:
        position = int(request.form['position'])
    except Exception:
        abort(400)

    submit_folder = f'{session["username"]}-{time.time()}'
    leader = board.acquire(position)
    path1 = f'{submissions_folder}/{leader}'
    path2 = f'{submissions_folder}/{submit_folder}'
    request.files['upload'].save(f'{path2}.zip')

    with ZipFile(f'{path2}.zip', 'r') as z:
        z.extractall(path2)

    if leader is None:
        board.replace(position, submit_folder)
        return 'Victory by default'

    uid = uuid.uuid4().hex
    build_path = f'{build_folder}/{uid}'

    shutil.copytree(template_folder, f'{build_path}/')
    copy_dir_contents(path1, f'{build_path}/p1')
    copy_dir_contents(path2, f'{build_path}/p2')
    shutil.copytree(server_folder, f'{build_path}/server')

    img = dock.images.build(path=build_path, tag=uid, rm=True, network_mode=None)
    container = dock.containers.run(uid, detach=True, auto_remove=True)

    lines = []
    maps = []
    errors = []

    for line in container.logs(stream=True):
        l = line.decode().strip()
        if 'ERROR:' == l[0:6]:
            errors.append(l[6:])
        elif 'MAP:' == l[0:4]:
            maps.append(l[4:])
        else:
            lines.append(l)

    lines = lines[3:]

    if 'Winner: p2' == lines[-1]:
        board.replace(position, submit_folder)

    board.release(position)

    game_id = database.logs.insert_one({'lines': lines,
                                        'maps': maps,
                                        'errors': errors,
                                        'build_id': uid,
                                        'defender': leader,
                                        'challenger': submit_folder,
                                        'submitter': session['username']}).inserted_id

    return jsonify(game_id=str(game_id))

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

@app.route('/api/getmatch', methods=['GET', 'POST'])
def getmatch():
    if not request.is_json:
        abort(400)

    body = request.get_json()

    if 'game_id' not in body:
        abort(400)

    result = database.logs.find_one({'_id': ObjectId(body['game_id'])})

    return jsonify(result['maps'])


@app.route('/api/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    return jsonify(list(map(lambda x: x.split('-')[0], board.board)))


@app.route('/api/isloggedin', methods=['GET', 'POST'])
def isloggedin():
    return str(logged_in())


@app.route('/api/isadmin', methods=['GET', 'POST'])
def isadmin():
    if not logged_in():
        return 'False'

    result = database.users.find_one({'username': session['username']})
    if result is None:
        return 'False'

    if 'admin' not in result or not result['admin']:
        return 'False'

    return 'True'

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

def login_guard():
    if 'logged_in' not in session or not session['logged_in']:
        abort(403)

def copy_dir_contents(src, dest):
    for file in os.listdir(src):
        shutil.copy(f'{src}/{file}', dest)

def logged_in():
    return session['logged_in'] if 'logged_in' in session else False
