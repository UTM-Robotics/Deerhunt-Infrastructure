import random, string, jwt

from flask_httpauth import HTTPTokenAuth

from passlib.hash import sha512_crypt
from datetime import datetime, timedelta

from server.Database import Mongo
from server.Models.User.GeneralUser import GeneralUserModel
from server.Managers.EmailBot.EmailBot import EmailBot

from server.config import Configuration
 

CODE_LENGTH = 16


def is_allowed(email: str) -> bool:
    """
    Checks to see if provided email has allowed domain.
    """
    for allowed_email in Configuration.MAIL_DOMAINS:
        if email.endswith(allowed_email):
            return True
    return False


User_auth = HTTPTokenAuth(scheme="Bearer")


@User_auth.verify_token
def verify_token(token):
    """
    Creates decorator function for checking General User Bearer token.
    Routes which have
                        @User_auth.login_required

    Call the verify_token() function below.
    """
    entry = Mongo.users.find_one({"jwt_token": token})
    if entry:
        try:
            jwt.decode(token, Configuration.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return False
        return entry["email"]
    return False


class UserManager:
    def __init__(self, email=None, code=None):
        self.db = Mongo.users
        self.user = GeneralUserModel(email, code)

    def __enter__(self):
        result = self.find_user() 
        if result:
            self.user.set_email(result["email"])
            self.user.set_password(result["password"])
            self.user.set_created_timestamp(result["created_timestamp"])
            self.user.set_code(result["code"])
            self.user.set_verified(result["verified"])
            self.user.set_jwt_token(result["jwt_token"])
            self.found = True
        else:
            self.found = False
        return self

    def __exit__(self, type, value, tb):
        pass

    def login(self, password):
        if self.found and self.user.verify_password(password):
            if not self.user.get_verified():
                return False
            now = datetime.utcnow()
            payload = {
                "iat": now,
                "exp": now + timedelta(minutes=60),
                "email": self.user.get_email(),
            }
            newToken = jwt.encode(payload, Configuration.SECRET_KEY, algorithm="HS256")
            self.user.set_jwt_token(newToken)
            self.commit()
            return newToken
        else:
            return False

    def delete(self):
        if self.found:
            if self.db.delete_one({"email": self.user.get_email()}):
                return True
            else:
                return False
        return False

    def update_password(self, old_password, new_password):
        if self.found and self.user.verify_password(old_password):
            self.user.set_password(sha512_crypt.hash(new_password))
            self.commit()
            return True
        return False

    def update_password_forgotten(self, new_password):
        if self.found:
            self.user.set_password(sha512_crypt.hash(new_password))
            self.generate_code(CODE_LENGTH)
            self.commit()
            return True
        return False

    def register(self, password):
        if not self.found:
            try:
                self.user.set_password(sha512_crypt.hash(password))
                self.user.set_created_timestamp(str(datetime.utcnow()))
                self.generate_code(CODE_LENGTH)
                self.commit()
                self.send_email("registration")
                return True
            except Exception:
                return False
        elif self.found and not self.user.verified:
            self.generate_code(CODE_LENGTH)
            self.commit()
            self.send_email("registration")
            return True
        else:
            return False

    def verify_code(self):
        """
        Checks if user link is expired.
        Expiration time is 30 minutes.
        Deletes user account entry if link expired.
        User has to register again if link expired.
        :return: bool
        """
        created_time = datetime.strptime(
            self.user.get_created_timestamp(), "%Y-%m-%d %H:%M:%S.%f"
        )
        curr_time = datetime.utcnow()
        time_delta = curr_time - created_time
        if time_delta.seconds < 1800:
            payload = {
                "iat": curr_time,
                "exp": curr_time + timedelta(minutes=60),
                "email": self.user.get_email(),
            }
            newToken = jwt.encode(payload, Configuration.SECRET_KEY, algorithm="HS256")
            self.user.set_jwt_token(newToken)
            self.user.set_verified(True)
            self.commit()
            return newToken
        else:
            self.db.delete_one({"code": self.user.get_code()})
            return False

    def generate_code(self, code_length) -> None:
        code = "".join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            )
            for _ in range(code_length)
        )
        self.user.set_code(code)

    def send_email(self, purpose: str):
        if purpose == "registration":
            with EmailBot() as emailbot:
                emailbot.build_message_registration(self.user.get_code())
                emailbot.send(self.user.get_email())
        elif purpose == "forgotpassword":
            with EmailBot() as emailbot:
                emailbot.build_message_forgotpassword(self.user.get_code())
                emailbot.send(self.user.get_email())
        return True

    def find_user(self):
        if self.user.get_email():
            return self.db.find_one({"email": self.user.get_email()})
        if self.user.get_code():
            x = self.db.find_one({"code": self.user.get_code()})
            return x
        return None

    def commit(self):
        query = {"email": self.user.get_email()}
        data = self.user.covert_to_dict()
        if self.found:
            self.db.update_one(query, {"$set": data})
        else:
            self.db.update_one(query, {"$setOnInsert": data}, upsert=True)
