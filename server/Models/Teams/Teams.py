class TeamsModel:
    def __init__(self, name):
        self.name = name
        self.members = []
        self.submission_id = None
        self.last_submission_timestamp = None
        self.created_timestamp = None

    def set_name(self, name) -> None:
        self.name = name
    
    def get_name(self) -> str:
        return self.name

    def add_member(self, email) -> None:
        self.members.append(email)

    def set_members(self, members: list) -> None:
        self.members = members
    
    def get_members(self) -> list:
        return self.members

    def set_submission_id(self, id) -> None:
        self.submission_id = id

    def get_submission_id(self) -> str:
        return self.submission_id

    def set_last_submission_timestamp(self, time) -> None:
        self.created_timestamp = time

    def get_last_submission_timestamp(self) -> str:
        return self.last_submission_timestamp

    def set_created_timestamp(self, time) -> None:
        self.created_timestamp = time

    def get_created_timestamp(self) -> str:
        return self.created_timestamp

    def covert_to_dict(self) -> dict:
        return {'name': self.get_name(),
                'members': self.get_members(),
                'submission_id': self.get_submission_id(),
                'last_submission': self.get_last_submission_timestamp(),
                'created_timestamp': self.get_created_timestamp()
                }
                