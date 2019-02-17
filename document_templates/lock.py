import time
import calendar

from enum import Enum

from pytz import timezone

from utils.time_utils import get_current_time_ms


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
        timezone=timezone("US/Eastern"),
        id="UNKNOWN",
        secret="",
    ):
        self.id = id
        self.status = status
        self.nickname = nickname
        self.passwords = passwords
        self.created_at = get_current_time_ms()
        self.timezone = timezone
        self.secret = secret

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
            "timezone": self.timezone.zone,
            "secret": self.secret,
        }

    @staticmethod
    def build(request_form):
        return Lock(
            nickname=request_form['nickname'],
            timezone=request_form['timezone'],
            secret=request_form['secret'],
        )
