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
    "email":  fields.Str(),
    "name":  fields.Str(missing=""),
}

POST_USER_LOCK_ARGS = {
    "ownedLockIds":  fields.DelimitedList(fields.Str()),
}

PUT_LOCK_STATUS = {
    "status":  EnumField(LockStatus, required=True),
    "lock_id": fields.Str(location='view_args', required=True),
}
