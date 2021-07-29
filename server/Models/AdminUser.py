from .User import UserModel

class AdminUserModel(UserModel):
    def __init__(self, username):
        super().__init__()
        self.username = username

    def set_username(self, username):
        self.username = username
    
    def get_username(self):
        return self.username

    def covert_to_dict(self) -> dict:
        return {'username': self.get_username(),
                'password': self.get_password(),
                'created_timestamp': self.get_created_timestamp(),
                'jwt_token': self.get_jwt_token()
                }
    