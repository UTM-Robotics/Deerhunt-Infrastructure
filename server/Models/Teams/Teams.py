from datetime import datetime
from typing import List

import re

email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


class TeamsModel:
    def __init__(self, name=None) -> None:
        self._id = None
        self.name = name
        self.owner = None
        self.members = []
        self.event_id = None
        self.last_submission_timestamp = None
        self.last_challenge_timestamp = None
        self.submissions: List[str] = []
        self.created_timestamp = None

    def set_id(self, team_id) -> None:
        self._id = team_id

    def get_id(self):
        return self._id

    def set_name(self, name) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name

    def set_owner(self, owner: str) -> None:
        if not re.fullmatch(email_regex, owner):
            raise TypeError("Must be a valid email")
        self.owner = owner

    def get_owner(self):
        return self.owner

    def set_members(self, members: List[str]) -> None:
        if len(members) > 4:
            raise ValueError("Must have less than or equal 4 members")
        self.members = members

    def get_members(self) -> List[str]:
        return self.members

    def set_event_id(self, event_id) -> None:
        self.event_id = event_id

    def get_event_id(self):
        return self.event_id

    def set_last_submission_timestamp(self, time) -> None:
        self.last_submission_timestamp = time

    def get_last_submission_timestamp(self) -> str:
        return self.last_submission_timestamp

    def set_last_challenge_timestamp(self, time):
        self.last_challenge_timestamp = time

    def get_last_challenge_timestamp(self):
        return self.last_challenge_timestamp

    def add_submission(self, submission: str) -> None:
        self.submissions.append(submission)

    def get_submissions(self) -> List[str]:
        return self.submissions

    def set_submissions(self, submissions: List[str]) -> None:
        self.submissions = submissions

    def set_created_timestamp(self, time) -> None:
        self.created_timestamp = time

    def get_created_timestamp(self) -> str:
        return self.created_timestamp

    def covert_to_dict(self) -> dict:
        if self.get_id():
            return {
                "_id": self.get_id(),
                "name": self.get_name(),
                "owner": self.get_owner(),
                "members": self.get_members(),
                "event_id": self.get_event_id(),
                "last_submission_timestamp": self.get_last_submission_timestamp(),
                "last_challenge_timestamp": self.get_last_challenge_timestamp(),
                "submissions": self.get_submissions(),
                "created_timestamp": self.get_created_timestamp(),
            }
        else:
            return {
                "name": self.get_name(),
                "owner": self.get_owner(),
                "members": self.get_members(),
                "event_id": self.get_event_id(),
                "last_submission_timestamp": self.get_last_submission_timestamp(),
                "last_challenge_timestamp": self.get_last_challenge_timestamp(),
                "submissions": self.get_submissions(),
                "created_timestamp": self.get_created_timestamp(),
            }
