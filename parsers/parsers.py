import time
import calendar

from webargs import fields
from parsers.enum_field import EnumField

from document_templates.lock import LockStatus

POST_ROUTE_ARGS = {
    "passwords":  fields.DelimitedList(missing=[]),
    "nickname":  fields.Str(missing="Smart Lock"),
    "status":  EnumField(LockStatus, missing=LockStatus.CLOSED),
    "createdAt": fields.Int(missing=calendar.timegm(time.gmtime())),
}
