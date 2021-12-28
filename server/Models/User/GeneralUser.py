from .User import UserModel

class GeneralUserModel(UserModel):
    def __init__(self, email=None, code=None):
        super().__init__()
        self.email = email
        self.code = code
        self.verified = False

    def set_email(self, email):
        self.email = email
    
    def get_email(self):
        return self.email

    def set_code(self, code):
        self.code = code

    def get_code(self):
        return self.code

    def set_verified(self, state: bool):
        self.verified = state
    
    def get_verified(self):
        return self.verified

    def covert_to_dict(self) -> dict:
        return {'email': self.get_email(),
                'password': self.get_password(),
                'code': self.get_code(),
                'created_timestamp': self.get_created_timestamp(),
                'verified': self.get_verified(),
                'jwt_token': self.get_jwt_token()
                }
    