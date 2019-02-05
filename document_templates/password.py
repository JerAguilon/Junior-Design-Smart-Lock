import time
import calendar

from enum import Enum

from utils.exceptions import AppException, ValidationException


class PasswordType(Enum):
    OTP = "OTP"
    PERMANENT = "PERMANENT"
    RECURRING = "RECURRING"


class PasswordMetadata(object):
    def __init__(
        self,
        type,
        expiration,
        id="UNKNOWN",
        created_at=calendar.timegm(time.gmtime())
    ):
        valid_for_null_expiration = {
            PasswordType.PERMANENT, PasswordType.OTP
        }
        if expiration is None:
            if type not in valid_for_null_expiration:
                raise ValidationException(
                    "Non-permanent passwords must specify an expiration"
                )
            expiration = -1

        self.type = type
        self.expiration = expiration
        self.id = id
        self.created_at = created_at

    def serialize(self):
        return {
            "type": str(self.type.value),
            "expiration": self.expiration,
            "id": self.id,
            "createdAt": self.created_at
        }

    @staticmethod
    def from_database(pw_id, password_dict):
        return PasswordMetadata(
            type=PasswordType(password_dict['type']),
            expiration=password_dict['expiration'],
            id=pw_id
        )


class Password(PasswordMetadata):
    def __init__(
        self,
        type,
        password,
        expiration=None,
        id="UNKNOWN",
    ):
        super().__init__(type, expiration, id)
        self.hashed_password = password

    def serialize(self):
        if self.id == "UNKNWON":
            raise AppException("An ID could not be created for this resource")
        return {
            "type": str(self.type.value),
            "password": self.hashed_password,
            "expiration": self.expiration,
            "createdAt": self.created_at
        }

    @staticmethod
    def build(request_form):
        return Password(
            type=PasswordType(request_form['type']),
            password=request_form['password'],
            expiration=request_form['expiration'],
        )
