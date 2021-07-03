from passlib.hash import sha512_crypt

class UserModel:
    def __init__(self, email, code):
        # self._id = None
        self.email = email
        self.password = None
        self.code = code
        self.jwt_token = None
        self.verified = False
        self.created_timestamp = None

    def set_email(self, email):
        self.email = email
    
    def get_email(self):
        return self.email

    def set_password(self, password):
        self.password = password

    def get_password(self):
        return self.password
    
    def verify_password(self, password):
        return sha512_crypt.verify(self.password, password)

    def set_code(self, code):
        self.code = code

    def get_code(self):
        return self.code

    def set_jwt_token(self, token):
        self.jwt_token = token

    def get_jwt_token(self):
        return self.jwt_token

    def set_verified(self, state: bool):
        self.verified = state
    
    def get_verified(self):
        return self.verified

    def set_created_timestamp(self, time):
        self.created_timestamp = time

    def get_created_timestamp(self):
        return self.created_timestamp

    def covert_to_dict(self) -> dict:
        return {'email': self.get_email(),
                'password': self.get_password(),
                'code': self.get_code(),
                'created_timestamp': self.get_created_timestamp(),
                'verified': self.get_verified()
                }
    