import time
import calendar

from enum import Enum

from utils.exceptions import ValidationException


class PasswordType(Enum):
    OTP = "OTP"
    PERMANENT = "PERMANENT"


class LockStatus(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    OPEN_REQUESTED = "OPEN_REQUESTED"


class Lock(object):
    def __init__(
        self,
        passwords,
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
            "status": str(self.status.value),
            "nickname": self.nickname,
            "passwords": [p.serialize() for p in self.passwords],
            "createdAt": self.created_at,
        }

    @staticmethod
    def build(request_form):
        return Lock([])


class Password(object):
    def __init__(self, type, hashed_password=None, salt=None, expiration=None):
        if expiration is None:
            if type != PasswordType.PERMANENT:
                raise ValidationException(
                    "Non-permanent passwords must specify an expiration"
                )
            expiration = -1

        self.type = type
        self.hashed_password = hashed_password
        self.salt = salt
        self.expiration = expiration

    def serialize(self):
        return {
            "type": str(self.type.value),
            "password": self.password
        }
