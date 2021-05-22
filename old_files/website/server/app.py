'''server/app.py - main api app declaration'''

import shutil
import os
import threading
import logging
from datetime import datetime
from zipfile import ZipFile, BadZipFile
from flask import Flask, jsonify, send_from_directory, request, abort, session, make_response
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from passlib.hash import sha512_crypt
from leaderboard import LeaderboardController
from email_bot import EmailBot
from tournament import TournamentController
from code_generator import CodeGenerator
from teams import TeamController
from global_state import GlobalController
from storage import StorageAPI
from challenge import ChallengeController
from consumer import Consumer

# import re


'''
Application Run Flags
'''
PROD_FLAG = False
# PROD_FLAG = False

'''Main wrapper for app creation'''
app = Flask(__name__, static_folder='../build')
app.config["MONGO_URI"] = "mongodb+srv://utmrobotics:1d3erhunted3089@deerhunt.ntpnz.mongodb.net/<dbname>?retryWrites=true&w=majority"
client = MongoClient(app.config["MONGO_URI"])
if PROD_FLAG:
    database = client.deerhunt_prod
    verification_domain = 'https://mcss.utmrobotics.com'
else:
    database = client.deerhunt_db
    verification_domain = 'localhost:8080'
#board = Leaderboard(database.leaderboard)
app.secret_key = b'a*\xfac\xd4\x940 m\xcf[\x90\x7f*P\xac\xcdk{\x9e3)e\xd7q\xd1n/>\xec\xec\xe0'
CORS(app)

# database = None
# dock = docker.from_env()

allowed_emails = ["@mail.utoronto.ca", "@utoronto.ca"]
codeGenerator = CodeGenerator(64)


prefix = '/deerhunt'
submissions_folder = f'{prefix}/submissions'
build_folder = f'{prefix}/build'
template_folder = f'{prefix}/template'
server_folder = f'{prefix}/server'

should_display_leaderboards = True
can_submit = True
submitting = {} # dict looks like: {'some team name': }

#Creates and runs the consumer thread for tournaments
#consumer = Consumer()
#consumer_thread = threading.Thread(target=consumer.run)
#consumer_thread.daemon = True
#consumer_thread.start()

# tournament_timer = threading.Thread(target=TournamentController.start_scheduler, args=(client, database, 3))
# t1 = TournamentController(client, database)
# t1.daemon = True
# t1.start()
# test = ['jasmine', 'kyrel', 'peter', 'jarvis', 'jack', 'raze', 'bufflin', 'dell', 'edmund', 'sova',
#         'jasmine2', 'kyrel2', 'peter2', 'jarvis2', 'jack2', 'raze2', 'bufflin2', 'dell2', 'edmund2', 'sova2',
#         'jasmine3', 'kyrel3', 'peter3', 'jarvis3', 'jack3', 'raze3', 'bufflin3', 'dell3', 'edmund3', 'sova3',
#         'jasmine4', 'kyrel4', 'peter4', 'jarvis4', 'jack4', 'raze4', 'bufflin4', 'dell4', 'edmund4']
        # 'jasmine5', 'kyrel5', 'peter5', 'jarvis5', 'jack5', 'raze5', 'bufflin5', 'dell5', 'edmund5', 'sova5',
        # 'jasmine6', 'kyrel6', 'peter6', 'jarvis6', 'jack6', 'raze6', 'bufflin6', 'dell6', 'edmund6', 'sova6',
        # 'jasmine7', 'kyrel7', 'peter7', 'jarvis7', 'jack7', 'raze7', 'bufflin7', 'dell7', 'edmund7', 'sova7',
        # 'jasmine8', 'kyrel8', 'peter8', 'jarvis8', 'jack8', 'raze8', 'bufflin8', 'dell8', 'edmund8', 'sova8']

##
# API routes
##


## Leaderboard and rank related routes.


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
    with TeamController(client, database) as team_api:
        team_document = team_api.get_user_team(session["username"])
        if team_document is None:
            abort(400)
    with StorageAPI(client, database) as s:
        if not s.save(request.files['upload'], team_document['_id']):
            if s.error == s.FAILED_EMPTY_FILE:
                return 'Cannot submit nothing :/'
            elif s.error == s.FAILED_NEED_MORE_TIME:
                return "Cannot submit within 5 minutes of last submission"
            elif s.error == s.FAILED_UPDATE_SUBMIT_TIME:
                abort(400)

    return "Zip submitted! Thanks"

@app.route('/api/lastsubmittime', methods=['GET'])
def get_last_submit():
    '''
    Instanstly saves a team's submission to /deerhunt/submissions/someTeamname/
    Also removes zip after extracting.
    '''

    with TeamController(client, database) as team_api:
        team_document = team_api.get_user_team(session["username"])
        if team_document is None:
            abort(400)
    if not "last_submitted" in team_document:
        abort(403)
    return {"last_submitted": team_document["last_submitted"]}

@app.route('/api/getqueue', methods=['GET'])
def get_queue():
    login_guard()
    sorted_queue = []
    result = database.submission_queue.find().sort('modified', 1)
    if result is None:
        abort(400)
    for match in result:
        challenger = database.teams.find_one({"_id": match['challenger_id']})
        defender = database.teams.find_one({"_id": match['defender_id']})
        temp = {}
        temp['challenger'] = challenger['displayName']
        temp['defender'] = defender['displayName']
        sorted_queue.append(temp)
    print(sorted_queue)
    return jsonify(sorted_queue)

@app.route('/api/canchallenge', methods=['GET'])
def can_challenge():
    """ Checks if the user is allowed to perform a challenge
    """
    login_guard()
    user = session['username']
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if "target_rank" not in data or data["target_rank"] is not int or data["target_rank"] <= 0:
        abort(400)
    target_rank = data["target_rank"]
    with ChallengeController(client, database) as challenge_api:
        if not challenge_api.can_challenge(user, target_rank):
            abort(400)
    return 

@app.route('/api/challenge', methods=['POST'])
def challenge():
    """ Allows the currently logged in user to challenge another user's rank.
        Follows the implication that if ranks are [A,B,C], if C beats A, ranks
        become [C,A,B]. Else, ranks are [A,B,C]
    """
    login_guard()
    user = session['username']
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if "target_rank" not in data or not isinstance(data["target_rank"], int) or data["target_rank"] < 0:
        abort(400)
    target_rank = data["target_rank"]
    with ChallengeController(client, database) as challenge_api:
        if not challenge_api.queue_challenge(user, target_rank):
            abort(400,challenge_api.error)
    return "OK"

@app.route('/api/scrimmage', methods=['POST'])
def scrimmage():
    ''' Runs a match against a player at a given position in the leaderboard without
    changing ranks.
    '''
    login_guard()
    user = session['username']
    if not request.is_json:
        abort(400)
    data = request.get_json()
    if "target_rank" not in data or not isinstance(data["target_rank"], int) or data["target_rank"] < 0:
        abort(400)
    target_rank = data["target_rank"]
    with ChallengeController(client, database) as challenge_api:
        if not challenge_api.do_scrimmage(user, target_rank):
            abort(400,challenge_api.error)
    return "Ok"

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
    return jsonify(result['data']['maps'])


@app.route("/api/teamgames", methods=['GET'])
def get_team_games():
    login_guard()
    with TeamController(client, database) as team_api:
        team_document = team_api.get_user_team(session["username"])
        if team_document is None:
            abort(400)
    ret = []
    result = database.logs.find({"$query":{"team_id": team_id}, "$orderby": {"_id": -1}})
    if result is None:
        return jsonify(ret)
    for log in result:
        ret.append(str(log["_id"]))
    return jsonify(ret)


@app.route('/api/rank', methods=['GET'])
def getrank():
    login_guard()
    with TeamController(client, database) as team_api:
        team = team_api.get_user_team(session["username"])
    if not team:
        abort(403)
    with LeaderboardController(client, database) as leaderboard_api:
        leaderboard = leaderboard_api.get_current_leaderboard()
        return {"rank":LeaderboardController.get_team_rank(leaderboard, team["name"])}
    abort(500)

@app.route('/api/leaderboard', methods=['GET'])
def get_current_leaderboard():
    ''' Gets the current leaderboard's state'''
    login_guard()

    with GlobalController(client, database) as global_api:
        if not global_api.get_leaderboard_state() or not global_api.ret_val:
            abort(403)

    with LeaderboardController(client,database) as leaderboard_api:
        leaderboard = leaderboard_api.get_current_leaderboard()
    if leaderboard is None:
        abort(500)

    lst = []
    teams = leaderboard["teams"]
    for team_name in teams:
        with TeamController(client,database) as team_api:
            team_doc = team_api.get_team(team_name)
        lst.append({'name': team_name,
            'display_name': team_doc["displayName"]
        })
    return jsonify(lst)

# Teams
# Teams assigning api calls


@app.route('/api/sendinvite', methods=['POST'])
def send_invite():
    '''Sends an invite from a user's current team to a user.'''
    login_guard()
    username = session["username"]
    if not request.is_json:
        abort(403)
    body = request.get_json()
    if not "recipient" in body:
        abort(403)
    recipient_doc = database.users.find_one({'username': body["recipient"]})
    if not recipient_doc:
        abort(403)
    with TeamController(client, database) as team_api:
        status = team_api.send_invite(username, body["recipient"])
    if not status:
        abort(409)
    return "Success"


@app.route('/api/userinvites', methods=['GET'])
def user_invites():
    """Gets the list of team display names and team names that a user
        has been invited to.
    """
    login_guard()
    with TeamController(client, database) as team_api:
        invites_team_dict = team_api.get_user_invites(session["username"])
    return invites_team_dict

# Teams assigning api calls


@app.route('/api/acceptinvite', methods=['POST'])
def accept_invite():
    '''Accpets an invite on a user's account, if the invite is valid.'''
    login_guard()
    username = session["username"]

    body = request.get_json()
    if not "team" in body:
        abort(400)

    with TeamController(client, database) as team_api:
        status = team_api.accept_invite(username, body["team"])
    if not status:
        abort(409)

    return "Success"


@app.route('/api/createteam', methods=['POST'])
def create_team():
    '''Creates a team if the team name is not taken, and the current logged-in
        user is not on a team.
    '''
    login_guard()
    if not request.is_json:
        abort(400)
    body = request.get_json()
    if not "team" in body:
        abort(400)

    with TeamController(client, database) as team_api:
        status = team_api.create_team(session["username"], body["team"])
    if not status:
        print("Request failed with error code:" + str(team_api.error))
        abort(409)
    return "Success"


@app.route('/api/leaveteam', methods=['POST'])
def leave_team():
    ''' Removes the current user from their team.'''
    login_guard()
    with TeamController(client, database) as team_api:
        status = team_api.leave_team(session["username"])
    if not status:
        print("Request failed with error code:" + str(team_api.error))
        abort(409)
    return "Success"


@app.route('/api/getteam', methods=['GET'])
def get_team():
    ''' Gets the current user's team'''
    login_guard()

    with TeamController(client, database) as team_api:
        team = team_api.get_user_team(session["username"])
    if not team:
        return {}
    team_json = {
        "name": team.get("name", ""),
        "display_name": team.get("displayName", ""),
        "invites":  team.get("invites", []),
        "users": team.get("users", [])
    }
    return team_json


@app.route('/api/getteaminvites', methods=['GET'])
def get_team_invites():
    ''' Gets the invites sent out by the team.'''
    login_guard()
    with TeamController(client, database) as team_api:
        team = team_api.get_user_team(session["username"])
    if not team:
        return {"invited_users": []}
    return {"invited_users": team.get("invites", [])}


@app.route('/api/reset', methods=['POST'])
def reset_password():
    user = safe_get_only_username()
    user = user.lower()
    user = user.strip(" ")
    result = database.users.find_one({'username': user})
    if result is None:
        abort(403)
    code = codeGenerator.generate()
    query = {'username': user}
    newvalues = {'$set': {'code': code, 'time': str(datetime.now())}}
    database.users.update_one(query, newvalues)
    msg = '\n\nPlease click on the link below to reset your password.\n\n{0}\n\nTechnical Team\nUTM Robotics'.format(
        "https://"+verification_domain+"/forgotpassword/"+code)
    email_status = EmailBot.sendmail(user, "BattleCode:Deerhunt Password Reset", msg)
    if not email_status:
        database.errors.insert_one({"error": "Email could not send, error ",
                                    'time': datetime.utcnow()
                                    })
        abort(400)
    return 'Reset link sent!'




@app.route('/api/login', methods=['POST'])
def login():
    ''' Checks the users inputs against database to validate for login.'''
    username, password = safe_get_user_and_pass()
    result = database.users.find_one({'username': username})
    if result is None or 'password' not in result:
        abort(403)

    if not sha512_crypt.verify(password, result['password']):
        abort(403)
    if result['verified'] == 'False':
        abort(403)

    session['logged_in'] = True
    session['username'] = username
    submitting[session['username']] = ''

    return 'Login successful'

# TODO: Tech-Debt: Proper Variable naming.
@app.route('/api/changepassword', methods=['GET', 'POST'])
def change_password():
    ''' Changes the current user's password.'''
    login_guard()

    cup, nep, cop = safe_get_passwords()
    result = database.users.find_one({'username': session['username']})
    if result is None:
        abort(403)
    if not sha512_crypt.verify(cup, result['password']):
        abort(403)
    if nep != cop:
        abort(400)
    query = {'username': session['username']}
    newvalues = {'$set': {'password': sha512_crypt.encrypt(nep)}}

    database.users.update_one(query, newvalues)

    return 'Change successful'

@app.route('/api/forgotpassword/<random>', methods=['GET', 'POST'])
def forgot_password(random):
    nep, cop, code= safe_get_reset_passwords()
    result = database.users.find_one({'code' : code})
    if result is None:
        abort(403)
    if nep != cop:
        abort(400)
    query = {'code': code}
    newvalues = {'$set': {'password': sha512_crypt.encrypt(nep)}}

    database.users.update_one(query, newvalues)

    return 'Reset successful'

@app.route('/verify/<code>')
def verify_email(code: str):
    '''Confirms a user's verification status based on their input.'''
    result = database.users.find_one({'code': code})
    if result is None:
        return "Invalid Verification Link."
    reg_time = datetime.strptime(result['time'], '%Y-%m-%d %H:%M:%S.%f')
    curr_time = datetime.now()
    time_delta = curr_time-reg_time
    if time_delta.seconds > 60*30:
        database.users.delete_one({"code": code})
        database.errors.insert_one({"error": "Deleting user account upon re-verification.",
                                    'time': datetime.utcnow(),
                                    "severity": "low"
                                    })
        return "Verification link has expired, Please recreate the account."
    query = {'code': code}
    newvalues = {'$set': {'verified': 'True'}}
    database.users.update_one(query, newvalues)
    return "Account has been verified successfully"


@app.route('/api/register', methods=['POST'])
def register():
    ''' Registers a user via their username and password if the inputs are valid.'''
    u, p = safe_get_user_and_pass()
    u = u.lower()
    u = u.strip(" ")
    result = database.users.find_one({'username': u})
    if result is not None:
        abort(409)

    if not is_allowed(u):
        abort(409)

    code = codeGenerator.generate()
    query = {'username': u}
    data = {'username': u,
            'password': sha512_crypt.encrypt(p),
            'code': code, 'time': str(datetime.now()),
            'verified': 'False'}
    write_result = database.users.update_one(
        query,
        {"$setOnInsert": data},
        upsert=True)
    if not write_result.upserted_id:
        abort(409)
    msg = '\n\nYour account has been successfully created. Please click the link below \
        to verify your account.\n\n{0}\n\nTechnical Team\nUTM Robotics'.format(
        verification_domain+"/verify/"+code)
    email_status = EmailBot.sendmail(u, "BattleCode:Deerhunt Account Verification", msg)
    if not email_status:
        database.errors.insert_one({"error": "Email could not send, error ",
                                    'time': datetime.utcnow(),
                                    "severity": "critical"
                                    })
        return abort(400)
    return 'Register successful'

@app.route('/api/isloggedin', methods=['GET', 'POST'])
def isloggedin():
    return str(logged_in())

# Admin access and Status


@app.route('/api/isadmin', methods=['GET', 'POST'])
def isadmin():
    """ Returns True iff a user is an admin."""
    return str(is_admin_check())

@app.route('/api/initglobalstate', methods=['POST'])
def initglobalstate():
    """ Initializes global state for the app."""
    admin_guard()
    with GlobalController(client, database) as globals_api:
        if not globals_api.init_state():
            abort(400)
    return str(True)

@app.route('/api/leaderboardtoggle', methods=['GET', 'POST'])
def leaderboardtoggle():
    if request.method == 'GET':
        with GlobalController(client, database) as globals_api:
            if not globals_api.get_leaderboard_state():
                abort(400)
        return str(globals_api.ret_val)
    admin_guard()

    with GlobalController(client, database) as globals_api:
        if not globals_api.leaderboard_toggle():
            abort(400)
    return str(globals_api.ret_val)


@app.route('/api/submittoggle', methods=['GET', 'POST'])
def submittoggle():
    if request.method == 'GET':
        with GlobalController(client, database) as globals_api:
            if not globals_api.get_submit_state():
                abort(400)
        return str(globals_api.ret_val)
    admin_guard()

    with GlobalController(client, database) as globals_api:
        if not globals_api.submit_toggle():
            abort(400)
    return str(globals_api.ret_val)


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

def safe_get_only_username():
    if not request.is_json:
        abort(400)
    body = request.get_json()
    return body['username']

def safe_get_user_and_pass():
    if not request.is_json:
        abort(400)

    body = request.get_json()

    return body['username'], body['password']

def safe_get_reset_passwords():

    if not request.is_json:
        return

    body = request.get_json()

    return body['newPassword'], body['confirmPassword'], body['code']


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


def is_allowed(email: str) -> bool:
    for allowed_email in allowed_emails:
        if email.endswith(allowed_email):
            return True
    return False


def copy_dir_contents(src, dest):
    for file in os.listdir(src):
        shutil.copy(f'{src}/{file}', dest)


if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    if PROD_FLAG:

        app.run(host='0.0.0.0', port=443) # The cert is included when gunicorn is called.
    else:
        app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
