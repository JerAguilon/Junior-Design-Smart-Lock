import time
import calendar

from enum import Enum

from utils.exceptions import AppException, ValidationException


class PasswordDays(Enum):
    SUNDAY = "SUNDAY"
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"

class PasswordType(Enum):
    OTP = "OTP"
    PERMANENT = "PERMANENT"
    RECURRING = "RECURRING"


class PasswordMetadata(object):
    def __init__(
        self,
        type,
        id="UNKNOWN",
        expiration=None,
        active_days=None,
        created_at=calendar.timegm(time.gmtime())
    ):
        self._validate_expiration(type, expiration)
        self._validate_active_days(type, active_days)

        if expiration is None:
            expiration = -1
        if active_days is None:
            active_days = []

        self.type = type
        self.expiration = expiration
        self.active_days = active_days
        self.id = id
        self.created_at = created_at

    def serialize(self):
        return {
            "id": self.id,
            "type": str(self.type.value),
            "expiration": self.expiration,
            "activeDays": self.active_days,
            "createdAt": self.created_at,
        }

    @staticmethod
    def from_database(pw_id, password_dict):
        return PasswordMetadata(
            type=PasswordType(password_dict['type']),
            expiration=password_dict['expiration'],
            id=pw_id
        )

    def _validate_expiration(self, type, expiration):
        valid_for_null_expiration = {
            PasswordType.PERMANENT, PasswordType.OTP
        }
        if expiration is None and type not in valid_for_null_expiration:
                raise ValidationException(
                    "Non-permanent passwords must specify an expiration"
                )

    def _validate_active_days(self, type, active_days):
        should_have_empty_active = {
            PasswordType.PERMANENT, PasswordType.OTP
        }
        if type in should_have_empty_active \
            and active_days is not None \
            and len(active_days) > 0:
            raise ValidationException(
                "Active days should be an empty list for pasword type {}".format(type.value)
            )



class Password(PasswordMetadata):
    def __init__(
        self,
        type,
        password,
        expiration=None,
        active_days=None,
        id="UNKNOWN",
    ):
        super().__init__(
            type=type,
            id=id,
            expiration=expiration,
        )
        self.hashed_password = password

    def serialize(self):
        if self.id == "UNKNWON":
            raise AppException("An ID could not be created for this resource")
        output = super().serialize()
        del output['id']  # Not necessary since the ID is a key
        output['password'] = self.hashed_password

        return output

    @staticmethod
    def build(request_form):
        return Password(
            type=PasswordType(request_form['type']),
            password=request_form['password'],
            expiration=request_form['expiration'],
        )
