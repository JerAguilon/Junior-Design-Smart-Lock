from enum import Enum

class PasswordType(Enum):
    OTP="OTP"
    PERMANENT="PERMANENT"

class Lock(object):
    def __init__(
        self,
        id,
        passwords
    ):
        self.id = id
        self.passwords = passwords

    def serialize(self):
        return {
            "id": self.id,
            "passwords": [p.serialize() for p in self.passwords]
        }

class Password(object):
    def __init__(self, type, password):
        self.type = type
        self.password = password

    def serialize(self):
        return {
            "type": str(self.type),
            "password": self.password
        }

