'''server/app.py - main api app declaration'''
import os
import uuid
import time
# import sched
import threading
import shutil
import schedule
# import docker
# import re
# import traceback
# from datetime import datetime
from zipfile import ZipFile, BadZipFile
from flask import Flask, jsonify, send_from_directory, request, abort, session
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from passlib.hash import sha512_crypt
from leaderboard import Leaderboard
from email_bot import EmailBot
from tournament import TournamentLevel

'''Main wrapper for app creation'''
app = Flask(__name__, static_folder='../build')
app.secret_key = b'a*\xfac\xd4\x940 m\xcf[\x90\x7f*P\xac\xcdk{\x9e3)e\xd7q\xd1n/>\xec\xec\xe0'
CORS(app)
database = MongoClient("mongodb+srv://utmrobotics:1d3erhunted3089@deerhunt.ntpnz.mongodb.net/<dbname>?retryWrites=true&w=majority").deerhunt_db
board = Leaderboard(database.leaderboard)
# dock = docker.from_env()
email_bot = EmailBot('aws.alertbot@gmail.com','5739842573') #Temperory email. TODO Change this.

prefix = '/deerhunt'
submissions_folder = f'{prefix}/submissions'
build_folder = f'{prefix}/build'
template_folder = f'{prefix}/template'
server_folder = f'{prefix}/server'

should_display_leaderboards = True
can_submit = True
submitting = {} # dict looks like: {'some team name': }


# Starting second thread for tournament timer.

def job():
    tourny = TournamentLevel(submitting)
    x = tourny.run()
    print(x)
# def run_threaded(job_func):
#     job_thread = threading.Thread(target=job_func)
#     job_thread.start()
# def runTournamentThread():
#     schedule.every(1).second.do(run_threaded, job)
#     while 1:
#         schedule.run_pending()
#         time.sleep(1)
# tournament_timer = threading.Thread(target=runTournamentThread)
# tournament_timer.start()
job()
##
# API routes
##

@app.route('/api/submit', methods=['POST'])
def submit():
    '''
    Instanstly saves a team's submission to /deerhunt/submissions/someTeamname/
    Also removes zip after extracting.
    '''
    login_guard()
    if not can_submit:
        abort(403)
    if 'upload' not in request.files:
        abort(400)
    # if session['username'] in submitting:
    #     shutil.rmtree(submitting[session['username']])
    submit_folder = f'{session["username"]}'
    submit_path = f'{submissions_folder}/{submit_folder}'
    request.files['upload'].save(f'{submit_path}.zip')
    submitting[session['username']] = submit_path
    try:
        with ZipFile(f'{submit_path}.zip', 'r') as z:
            z.extractall(submit_path)
    except BadZipFile:
        abort(400)
    os.remove(f'{submit_path}.zip')    
    return "Zip submitted! Thanks"

    # try:
    #     position = int(request.form['position']) - 1
    # except Exception:
    #     abort(400)

    # if position < 0 or position > 9:
    #     abort(400)

    # try:
    #     result = run_match(position)
    # except Exception as e:
    #     database.errors.insert_one({'message': str(e), 'trace': traceback.format_exc(),'time': datetime.utcnow()})

    #     if board.is_locked(position):
    #         board.release(position)

    #     abort(500)
    # finally:
    #     submitting[session['username']] = False

    
@staticmethod
def run_match(position):
    leader = board.acquire(position)
    leader_path = f'{submissions_folder}/{leader}'

    if leader is None:
        board.replace(position, submit_folder)
        board.save('default')
        return 'Victory by default'

    uid = uuid.uuid4().hex
    build_path = f'{build_folder}/{uid}'

    shutil.copytree(template_folder, f'{build_path}/')
    copy_dir_contents(leader_path, f'{build_path}/p1')
    copy_dir_contents(submit_path, f'{build_path}/p2')
    shutil.copytree(server_folder, f'{build_path}/server')

    img = dock.images.build(path=build_path, tag=uid, rm=True, network_mode=None)
    container = dock.containers.run(uid, detach=True, auto_remove=True, network_mode=None,
                                    cpu_count=1, mem_limit='512m')

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
        board.save(uid)

    board.release(position)

    game_id = database.logs.insert_one({'lines': lines,
                                        'maps': maps,
                                        'errors': errors,
                                        'build_id': uid,
                                        'defender': leader,
                                        'challenger': submit_folder,
                                        'submitter': session['username']}).inserted_id

    return jsonify(game_id=str(game_id), message=lines[-1])



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
    submitting[session['username']] = False

    return 'Login successful'

@app.route('/api/changepassword', methods=['GET', 'POST'])
def changePassword():
    login_guard()

    cup, nep, cop = safe_get_passwords()

    result = database.users.find_one({'username': session['username']})
    if result is None or 'password' not in result:
        abort(403)
    if not sha512_crypt.verify(cup, result['password']):
        abort(403)
    if nep != cop:
        abort(400)

    query = {'username': session['username']}
    newvalues = {'$set': {'password': sha512_crypt.encrypt(nep)}}

    database.users.update_one(query, newvalues)

    return 'Change successful'

@app.route('/api/register', methods=['POST'])
def register():
    #admin_guard()

    u, p = safe_get_user_and_pass()

    result = database.users.find_one({'username': u})
    if result is not None:
        abort(409)

    database.users.insert_one({'username': u,
                               'password': sha512_crypt.encrypt(p)})

    return 'Register successful'

@app.route('/api/getmatch', methods=['GET', 'POST'])
def getmatch():
    login_guard()

    if not request.is_json:
        abort(400)

    body = request.get_json()

    if 'game_id' not in body:
        abort(400)

    result = database.logs.find_one({'_id': ObjectId(body['game_id'])})

    if result is None:
        abort(400)

    return jsonify(result['maps'])


@app.route('/api/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    login_guard()

    if not should_display_leaderboards:
        abort(403)

    lst = []
    for i in range(len(board.board)):
        lst.append({
            'name': board.board[i].split('-')[0],
            'queue': board.queue_count[i]
        })

    return jsonify(lst)

@app.route('/api/isloggedin', methods=['GET', 'POST'])
def isloggedin():
    return str(logged_in())


@app.route('/api/isadmin', methods=['GET', 'POST'])
def isadmin():
    return str(is_admin_check())

@app.route('/api/leaderboardtoggle', methods=['GET', 'POST'])
def leaderboardtoggle():
    global should_display_leaderboards

    if request.method == 'GET':
        return str(should_display_leaderboards)

    admin_guard()

    should_display_leaderboards = not should_display_leaderboards
    return str(should_display_leaderboards)


@app.route('/api/submittoggle', methods=['GET', 'POST'])
def submittoggle():
    global can_submit
    if request.method == 'GET':
        return str(can_submit)

    admin_guard()

    can_submit = not can_submit
    return str(can_submit)

@app.route('/api/resetlockout', methods=['GET', 'POST'])
def resetlockout():
    admin_guard()

    if not request.is_json:
        abort(400)

    body = request.get_json()

    if 'username' not in body:
        abort(400)

    if body['username'] in submitting:
        submitting[body['username']] = False

    return 'Success'

##
# View route
##

@app.route('/tutorial')
def tutorial():
  #pylint: disable=unused-argument
  return send_from_directory(app.static_folder, 'tutorial.html')


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

def safe_get_passwords():
    if not request.is_json:
        abort(400)

    body = request.get_json()

    return body['currentPassword'], body['newPassword'], body['confirmPassword']

def login_guard():
    if 'logged_in' not in session or not session['logged_in']:
        abort(403)

def logged_in():
    return session['logged_in'] if 'logged_in' in session else False

def admin_guard():
    if not is_admin_check():
        abort(403)

def is_admin_check():
    if not logged_in():
        return False

    result = database.users.find_one({'username': session['username']})
    if result is None:
        return False

    if 'admin' not in result or not result['admin']:
        return False

    return True

def copy_dir_contents(src, dest):
    for file in os.listdir(src):
        shutil.copy(f'{src}/{file}', dest)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7082, threaded=True, debug=True)