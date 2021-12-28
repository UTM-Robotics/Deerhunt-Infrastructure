class TeamsModel:
    def __init__(self, name, owner) -> None:
        self.name = name
        self.owner = owner
        self.members = []
        self.eventID = None
        self.last_submission_timestamp = None
        self.created_timestamp = None

    def add_member(self, email) -> None:
        self.members.append(email)

    def set_members(self, members: list) -> None:
        self.members = members
    
    def get_members(self) -> list:
        return self.members
    
    def join_event(self, eventID: str) -> None:
        self.eventID = eventID

    def set_last_submission_timestamp(self, time) -> None:
        self.created_timestamp = time

    def set_created_timestamp(self, time) -> None:
        self.created_timestamp = time

    def covert_to_dict(self) -> dict:
        return {'name': self.name,
                'owner': self.owner,
                'members': self.members,
                'eventID': self.eventID,
                'last_submission': self.last_submission_timestamp,
                'created_timestamp': self.created_timestamp
                }
                