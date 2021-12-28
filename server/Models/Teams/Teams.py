class TeamsModel:
    def __init__(self, name) -> None:
        self.name = name
        self.owner = None
        self.members = []
        self.eventID = None
        self.last_submission_timestamp = None
        self.created_timestamp = None
    
    def set_owner(self, owner) -> None:
        self.owner = owner

    def set_members(self, members: list) -> None:
        self.members = members
    
    def get_members(self) -> list:
        return self.members
    
    def join_event(self, eventID: str) -> None:
        self.eventID = eventID

    def set_last_submission_timestamp(self, time) -> None:
        self.last_submission_timestamp = time

    def set_created_timestamp(self, time) -> None:
        self.created_timestamp = time

    def covert_to_dict(self) -> dict:
        return {'name': self.name,
                'owner': self.owner,
                'members': self.members,
                'eventID': self.eventID,
                'last_submission_timestamp': self.last_submission_timestamp,
                'created_timestamp': self.created_timestamp
                }
                