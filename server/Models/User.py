from ..app import Mongo
from passlib.hash import sha512_crypt

class UserModel:
    def __init__(self, email=None, password=None, code=None):
        self.db = Mongo
        self.email = email
        if password is not None:
            self.password = sha512_crypt.encrypt(password)
        else:
            self.password = password
        self.code = code
        self.verified = False

    def set_email(self, email):
        self.email = email
    
    def get_email(self):
        return self.email

    def set_password(self, password):
        self.password = sha512_crypt(password)
    
    def verify_password(self, password):
        return sha512_crypt.verify(self.password, password)

    def set_code(self, code):
        self.code = code

    def get_code(self):
        return self.code

    def verify(self):
        pass

    def find_user_by_email(self):
        return self.db.users.find_one({'email': self.email})

    def find_user_by_code(self, code):
        return self.db.users.find_one({'code': self.code})
    

    