import time
import calendar

from enum import Enum
from typing import Dict

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
    UNLIMITED = "UNLIMITED"


class PasswordMetadata(object):
    def __init__(
        self,
        type,
        id="UNKNOWN",
        expiration=None,
        active_days=None,
        created_at=calendar.timegm(time.gmtime())
    ):
        PasswordMetadata.validate_expiration(type, expiration)
        PasswordMetadata.validate_active_days(type, active_days)

        if expiration is None:
            expiration = -1
        if active_days is None:
            active_days = []

        self.type = type
        self.expiration = expiration
        self.active_days = active_days
        self.id = id
        self.created_at = created_at

    def serialize(self, include_id=True):
        PasswordMetadata.validate_expiration(self.type, self.expiration)
        PasswordMetadata.validate_active_days(self.type, self.active_days)
        output = {
            "type": str(self.type.value),
            "expiration": self.expiration,
            "activeDays": [d.value for d in self.active_days],
            "createdAt": self.created_at,
        }
        if include_id:
            output['id'] = self.id
        return output

    def update(self, update_args: Dict[str, str]):
        if 'expiration' in update_args:
            self.expiration = update_args['expiration']
        if 'activeDays' in update_args:
            self.active_days = [
                PasswordDays(d) for d in update_args['activeDays']
            ]

    @staticmethod
    def from_database(pw_id, password_dict):
        return PasswordMetadata(
            type=PasswordType(password_dict['type']),
            expiration=password_dict['expiration'],
            active_days=[
                PasswordDays(d) for d in password_dict.get('activeDays', [])
            ],
            created_at=password_dict['createdAt'],
            id=pw_id
        )

    @staticmethod
    def validate_expiration(type, expiration):
        if type == PasswordType.OTP and expiration is not None:
            raise ValidationException(
                "OTP passwords should not have an expiration specified"
            )

    @staticmethod
    def validate_active_days(type, active_days):
        validation_error_template = (
            "Active days should be an empty list for password type {}"
        )
        if type == PasswordType.OTP \
                and active_days is not None \
                and len(active_days) > 0:
            raise ValidationException(
                validation_error_template.format(type.value))


class Password(PasswordMetadata):
    def __init__(
        self,
        password,
        **kwargs,
    ):
        super().__init__(**kwargs)
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

    def update(self, update_args: Dict[str, str]):
        super().update(update_args)
        if 'password' in update_args:
            self.hashed_password = update_args['password']

    @staticmethod
    def from_database(pw_id, password_dict):
        return Password(
            type=PasswordType(password_dict['type']),
            expiration=password_dict['expiration'],
            active_days=[
                PasswordDays(d) for d in password_dict.get('activeDays', [])
            ],
            created_at=password_dict['createdAt'],
            password=password_dict['password'],
            id=pw_id,
        )
