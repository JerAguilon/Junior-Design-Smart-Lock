import time
import calendar

from webargs import fields

from document_templates.lock import LockStatus
from parsers.enum_field import EnumField
from parsers.parser_utils import swagger_input_model

POST_LOCKS_ARGS = {
    "passwords": fields.DelimitedList(
        fields.Str(),
        missing=[],
        description="A list of passwords to initialize the lock with",
        required=False
    ),
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

POST_USER_LOCK_ARGS = {
    "ownedLockIds": fields.DelimitedList(
        fields.Str(),
        description="A list of lock ids to add to the user",
        required=True
    ),
}


PUT_LOCK_STATUS_ARGS = {
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
class PutLockStatusArgs(object):
    resource_fields = PUT_LOCK_STATUS_ARGS
