import time
import calendar

from enum import Enum


class LockStatus(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    OPEN_REQUESTED = "OPEN_REQUESTED"


class Lock(object):
    def __init__(
        self,
        passwords={},
        nickname="Smart Lock",
        status=LockStatus.CLOSED,
        created_at=calendar.timegm(time.gmtime()),
        id="UNKNOWN"
    ):
        self.id = id
        self.status = status
        self.nickname = nickname
        self.passwords = passwords
        self.created_at = created_at

    def serialize(self):
        return {
            "status": str(
                self.status.value),
            "nickname": self.nickname,
            "passwords": dict(
                (pw_id,
                 pw.serialize()) for (
                    pw_id,
                    pw) in self.passwords.items()),
            "createdAt": self.created_at,
        }

    @staticmethod
    def build(request_form):
        return Lock()
