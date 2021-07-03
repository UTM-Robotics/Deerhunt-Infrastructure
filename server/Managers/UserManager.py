import random, string

from passlib.hash import sha512_crypt
from datetime import datetime

from server.Database import Mongo
from server.Models.UserModel import UserModel
from server.Managers.EmailBot.EmailBot import EmailBot

from server.config import Configuration


CODE_LENGTH = 8


def is_allowed(email: str) -> bool:
    '''
    Checks to see if provided email has allowed domain.
    '''
    for allowed_email in Configuration.MAIL_DOMAINS:
        if email.endswith(allowed_email):
            return True
    return False


class UserManager:

    def __init__(self, email=None, code=None):
        self.db = Mongo.users
        self.user = UserModel(email, code)

    def __enter__(self):
        result = self.find_user()
        if result:
            # self.user.set_id(result['_id'])
            self.user.set_email(result['email'])
            self.user.set_password(result['password'])
            self.user.set_created_timestamp(result['created_timestamp'])
            self.user.set_code(result['code'])
            self.found = True
        else:
            self.found = False
        return self

    def __exit__(self, type, value, tb):
        pass

    def login(self, password):
        if self.user.verify_password(password):
            pass
            # make jwt token
            return
        else:
            return False
    
    
    def register(self, password):
        try:
            self.user.set_password(sha512_crypt.hash(password))
            self.user.set_created_timestamp(str(datetime.now()))
            self.generate_code(CODE_LENGTH)
            self.commit()
            self.send_email('registration')
            return True
        except Exception:
            return False


    def verify_code(self):
        self.user.set_verified(True)
        self.commit()
        return True


    def generate_code(self, code_length) -> None:
        code = ''.join(random.choice(string.ascii_uppercase + 
                                  string.ascii_lowercase + 
                                  string.digits) for _ in range(code_length))
        self.user.set_code(code)


    def send_email(self, purpose: str):
        if purpose == 'registration':
            with EmailBot() as emailbot:
                emailbot.build_message_registration(self.user.get_code())
                emailbot.send(self.user.get_email())
        elif purpose == 'password_reset':
            pass
    

    def find_user(self):
        if self.user.get_email():
            return self.db.find_one({'email': self.user.get_email()})
        if self.user.get_code():
            x = self.db.find_one({'code': self.user.get_code()})
            return x
        return None


    def commit(self):
        query = {'email': self.user.get_email()}
        data = self.user.covert_to_dict()
        if self.found:
            self.db.update_one(query, {'$set': data })
        else:
            self.db.update_one(query, {"$setOnInsert": data}, upsert=True)
