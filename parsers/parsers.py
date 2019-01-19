import time
import calendar

from webargs import fields
from parsers.enum_field import EnumField

from document_templates.lock import LockStatus

POST_LOCKS_ARGS = {
    "passwords":  fields.DelimitedList(
        fields.Str(),
        missing=[],
        description="A list of passwords to initialize the lock with",
        required=False
    ),
    "nickname":  fields.Str(
        missing="Smart Lock",
        description="A readable nickname for the lock",
        required=False
    ),
    "status":  EnumField(
        LockStatus,
        missing=LockStatus.CLOSED,
        description="A lock status to initialize the lock to",
        required=False
    ),
    "createdAt": fields.Int(
        missing=calendar.timegm(time.gmtime()),
        description="The unix milliseconds since epoch in which the lock was registered",
        required=False,
    ),
}

POST_USER_ARGS = {
    "email":  fields.Str(
        description="The email of the user",
        required=True,
    ),
    "name":  fields.Str(
        missing="",
        description="The name of the user",
        required=False
    ),
}

POST_USER_LOCK_ARGS = {
    "ownedLockIds":  fields.DelimitedList(
        fields.Str(),
        description="A list of lock ids to add to the user",
        required=True
    ),
}

PUT_LOCK_STATUS = {
    "status":  EnumField(
        LockStatus,
        description="The latest lock status to update to",
        required=True
    ),
    "lock_id": fields.Str(
        location='view_args',
        description='A unique lock id',
        required=True
    ),
}
