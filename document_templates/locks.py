from enum import Enum
from utils.decorators import require_fields

class PasswordType(Enum):
    OTP="OTP"
    PERMANENT="PERMANENT"

class LockStatus(Enum):
    CLOSED="CLOSED"

class Lock(object):
    def __init__(
        self,
        passwords,
        nickname="Smart Lock",
        status=LockStatus.CLOSED,
    ):
        self.status = status.closed
        self.nickname=nickname
        self.passwords = passwords

    def serialize(self):
        return {
            "status": str(self.status.value),
            "nickname": self.nickname,
            "passwords": [p.serialize() for p in self.passwords]
        }

    @staticmethod
    @require_fields([])
    def build(request_form):
        return Lock([])

class Password(object):
    def __init__(self, type, password):
        self.type = type
        self.password = password

    def serialize(self):
        return {
            "type": str(self.type.value),
            "password": self.password
        }

