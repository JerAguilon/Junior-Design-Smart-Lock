from __future__ import unicode_literals

import sys
import warnings
from enum import Enum

from marshmallow import ValidationError
from marshmallow.fields import Field
from pytz import timezone

from utils.exceptions import ValidationException

PY2 = sys.version_info.major == 2
# ugh Python 2
if PY2:
    string_types = (str, unicode)  # noqa: F821
    text_type = unicode  # noqa: F821
else:
    string_types = (str, )
    text_type = str


class LoadDumpOptions(Enum):
    value = 1
    name = 0


class EnumField(Field):
    def __init__(self, klass, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.klass = klass

    def _serialize(self, value, attr, obj, **kwargs):
        return value.value

    def _deserialize(self, value, attr, obj, **kwargs):
        try:
            return self.klass(value)
        except Exception:
            raise ValidationException("Invalid value for {}: {}".format(
                self.klass, value))


class TimezoneField(Field):

    def _serialize(self, value, attr, obj, **kwargs):
        return value.zone

    def _deserialize(self, value, attr, obj, **kwargs):
        try:
            return timezone(value)
        except Exception as e:
            raise ValidationException("Invalid timezone: {}".format(value))
