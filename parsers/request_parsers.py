import time
import calendar

from webargs import fields

from document_templates.lock import LockStatus
from document_templates.password import PasswordType
from parsers.enum_field import EnumField
from parsers.parser_utils import swagger_input_model


@swagger_input_model
class PostLocksArgs(object):
    resource_fields = {
        "nickname": fields.Str(
            missing="Smart Lock",
            description="A readable nickname for the lock",
            required=False
        ),
        "status": EnumField(
            LockStatus,
            missing=LockStatus.CLOSED,
            description="A lock status to initialize the lock to",
            required=False
        ),
        "createdAt": fields.Int(
            missing=calendar.timegm(time.gmtime()),
            description=("The unix milliseconds since epoch in "
                         "which the lock was registered"),
            required=False,
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
        "type": EnumField(
            PasswordType,
            description='The type of the password',
            required=False
        ),
        "password": fields.Str(
            description='The six digit password',
            required=False,
            validate=lambda p: len(p) == 6 and p.isdigit(),
        ),
        "expiration": fields.Int(
            description='The ms since unix epoch to expire the password',
            required=False,
        )
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
        "expiration": fields.Int(
            description='The ms since unix epoch to expire the password',
            required=False,
            missing=None,
        )
    }
