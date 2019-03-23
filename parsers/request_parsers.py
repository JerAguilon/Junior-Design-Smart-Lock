import re

from webargs import fields

from document_templates.lock import LockStatus
from document_templates.password import PasswordType, PasswordDays
from parsers.field_utils import EnumField, TimezoneField
from parsers.parser_utils import swagger_input_model


@swagger_input_model
class DeleteUserLockArgs(object):
    resource_fields = {
        "lockId": fields.Str(
            location='view_args',
            description='A unique lock id',
            required=True
        ),
    }


@swagger_input_model
class PostLocksArgs(object):
    resource_fields = {
        "nickname": fields.Str(
            missing="Smart Lock",
            description="A readable nickname for the lock",
            required=False
        ),
        "timezone": TimezoneField(
            missing='US/Eastern',
            description=("The timezone of the lock's location. "
                         "Important for functionality like recurring "
                         "passwords."),
            required=False,
        ),
        "secret": fields.Str(
            description="A secret key for the lock",
            required=True
        ),
    }


@swagger_input_model
class PostUserLockArgs(object):
    resource_fields = {
        "ownedLockIds": fields.DelimitedList(
            fields.Str(),
            description="A list of lock ids to add to the user",
            required=True
        ),
    }


@swagger_input_model
class PutHardwareLockStatusArgs(object):
    resource_fields = {
        "status": EnumField(
            LockStatus,
            description="The latest lock status to update to",
            required=True
        ),
    }


@swagger_input_model
class PutLockStatusArgs(object):
    resource_fields = {
        "status": EnumField(
            LockStatus,
            description="The latest lock status to update to",
            required=True
        ),
        "lockId": fields.Str(
            location='view_args',
            description='A unique lock id',
            required=True
        ),
        "password": fields.Str(
            description='A valid password if requesting to open',
            required=False,
            validate=lambda p: len(p) == 6 and p.isdigit(),
        )
    }


@swagger_input_model
class GetLockHistoryArgs(object):
    resource_fields = {
        "lockId": fields.Str(
            location='view_args',
            description='A unique lock id',
            required=True
        ),
    }


@swagger_input_model
class GetLockPasswordMetadataArgs(object):
    resource_fields = {
        "lockId": fields.Str(
            location='view_args',
            description='A unique lock id',
            required=True
        ),
        "passwordId": fields.Str(
            location='view_args',
            description='A unique password id',
            required=True
        ),
    }


@swagger_input_model
class PutLockPasswordArgs(object):
    resource_fields = {
        "password": fields.Str(
            description='The six digit password',
            required=False,
            validate=lambda p: len(p) == 6 and p.isdigit(),
        ),
        "expiration": fields.Int(
            description='The ms since unix epoch to expire the password',
            required=False,
        ),
        "activeDays": fields.DelimitedList(
            EnumField(PasswordDays),
            description='A list of the days that the password is available',
            required=False,
        ),
        "activeTimes": fields.DelimitedList(
            fields.Str(
                description='A time formatted as HH:MM',
                validate=lambda s: re.fullmatch(s, '([0-1]?[0-9]|2[0-3]):[0-5][0-9]')
            ),
            description='A list of two times (local to the lock) in HH:MM format for when the password is active.',
            validate=lambda l: len(l) == 2,
            required=False,
            missing=[],
        ),
    }


@swagger_input_model
class PostLockPasswordsArgs(object):
    resource_fields = {
        "lockId": fields.Str(
            location='view_args',
            description='A unique lock id',
            required=True
        ),
        "type": EnumField(
            PasswordType,
            description='The type of the password',
            required=True
        ),
        "password": fields.Str(
            description='The six digit password',
            required=True,
            validate=lambda p: len(p) == 6 and p.isdigit(),
        ),
        "activeDays": fields.DelimitedList(
            EnumField(PasswordDays),
            description='A list of the days that the password is available',
            required=False,
            missing=[],
        ),
        "activeTimes": fields.DelimitedList(
            fields.Str(
                description='A time formatted as HH:MM',
                validate=lambda s: re.fullmatch(s, '([0-1]?[0-9]|2[0-3]):[0-5][0-9]')
            ),
            description='A list of two times (local to the lock) in HH:MM format for when the password is active.',
            validate=lambda l: len(l) == 2,
            required=False,
            missing=[],
        ),
        "expiration": fields.Int(
            description='The ms since unix epoch to expire the password',
            required=False,
            missing=None,
        ),
    }
