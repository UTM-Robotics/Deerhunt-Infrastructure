from datetime import datetime
from typing import List

import re

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class TeamsModel:
    def __init__(self, name) -> None:
        self.name = name
        self.owner = None
        self.members = []
        self.event_id = None
        self.last_submission_timestamp = None
        self.submissions: List[str] = []
        self.created_timestamp = None
        self.uuid = None

    def __init__(self) -> None:
        self.name = None
        self.owner = None
        self.members = []
        self.eventID = None
        self.last_submission_timestamp = None
        self.submissions: List[str] = []
        self.created_timestamp = None
        self.uuid = None

    def set_owner(self, owner: str) -> None:
        if not re.fullmatch(email_regex, owner):
            raise TypeError("Must be a valid email")
        self.owner = owner

    def set_members(self, members: List[str]) -> None:
        if len(members) > 4:
            raise ValueError("Must have less than or equal 4 members")
        self.members.extend(members)

    def get_members(self) -> List[str]:
        return self.members

    def join_event(self, event_id: str) -> None:
        self.event_id = event_id

    def get_last_submission_timestamp(self) -> str:
        return self.last_submission_timestamp

    def set_last_submission_timestamp(self, time) -> None:
        self.last_submission_timestamp = time

    def set_created_timestamp(self, time) -> None:
        self.created_timestamp = time

    def set_uuid(self, uuid) -> None:
        self.uuid = uuid

    def get_uuid(self) -> str:
        return self.uuid

    def get_submissions(self) -> List[str]:
        return self.submissions

    def set_submissions(self, submissions: List[str]) -> None:
        self.submissions = submissions

    def add_submission(self, submission: str) -> None:
        self.submissions.append(submission)

    def set_name(self, name) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name

    def covert_to_dict(self) -> dict:
        return {'name': self.name,
                'owner': self.owner,
                'members': self.members,
                'event_id': self.event_id,
                'uuid': self.uuid,
                'last_submission_timestamp': self.last_submission_timestamp,
                'submissions': self.submissions,
                'created_timestamp': self.created_timestamp
                }
