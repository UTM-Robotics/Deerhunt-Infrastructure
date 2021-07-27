from passlib.hash import sha512_crypt

class AdminModel:
    def __init__(self, username):
        self.username = username
        self.password = None
        self.jwt_token = None
        self.created_timestamp = None

    def set_username(self, username):
        self.username = username
    
    def get_username(self):
        return self.username

    def set_password(self, password):
        self.password = password

    def get_password(self):
        return self.password
    
    def verify_password(self, password):
        return sha512_crypt.verify(password, self.password)

    def set_jwt_token(self, token):
        self.jwt_token = token

    def get_jwt_token(self):
        return self.jwt_token

    def set_created_timestamp(self, time):
        self.created_timestamp = time

    def get_created_timestamp(self):
        return self.created_timestamp

    def covert_to_dict(self) -> dict:
        return {'username': self.get_username(),
                'password': self.get_password(),
                'created_timestamp': self.get_created_timestamp(),
                'jwt_token': self.get_jwt_token()
                }
    