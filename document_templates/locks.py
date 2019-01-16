from enum import Enum

class PasswordType(Enum):
    OTP="OTP"
    PERMANENT="PERMANENT"

class LockStatus(Enum):
    CLOSED="CLOSED"

class Lock(object):
    def __init__(
        self,
        passwords,
        status=LockStatus.CLOSED,
    ):
        self.status = status.closed
        self.passwords = passwords

    def serialize(self):
        return {
            "status": str(self.status.value),
            "passwords": [p.serialize() for p in self.passwords]
        }

class Password(object):
    def __init__(self, type, password):
        self.type = type
        self.password = password

    def serialize(self):
        return {
            "type": str(self.type.value),
            "password": self.password
        }

