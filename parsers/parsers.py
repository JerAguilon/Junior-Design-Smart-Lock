import time
import calendar

from webargs import fields
from parsers.enum_field import EnumField

from document_templates.lock import LockStatus

POST_LOCKS_ARGS = {
    "passwords":  fields.DelimitedList(fields.Str(), missing=[]),
    "nickname":  fields.Str(missing="Smart Lock"),
    "status":  EnumField(LockStatus, missing=LockStatus.CLOSED),
    "createdAt": fields.Int(missing=calendar.timegm(time.gmtime())),
}

POST_USER_ARGS = {
    "email":  fields.Str(),
    "name":  fields.Str(missing=""),
}

POST_USER_LOCK_ARGS = {
    "ownedLockIds":  fields.DelimitedList(fields.Str()),
}

PUT_LOCK_STATUS = {
    "status":  EnumField(LockStatus),
    "lock_id": fields.Str(location='view_args', required=True),
}
