from __future__ import unicode_literals

from enum import Enum

from marshmallow.fields import Field
from pytz import timezone

from utils.exceptions import ValidationException



class LoadDumpOptions(Enum):
    value = 1
    name = 0


class EnumField(Field):
    def __init__(self, klass, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.klass = klass
        self.values = [k.value for k in klass]
        error = 'Provided enum was invalid. Make sure it is one of {}'.format(
                self.values)
        self.default_error_messages = {
            'invalid': error,
            'error': error,
        }

    def _serialize(self, value, attr, obj, **kwargs):
        return value.value

    def _deserialize(self, value, attr, obj, **kwargs):
        message = "Invalid value for {}. Make sure it is one of {}".format(
            value, self.values
        )
        try:
            return self.klass(value)
        except Exception:
            raise ValidationException(message)


class TimezoneField(Field):

    def _serialize(self, value, attr, obj, **kwargs):
        return value.zone

    def _deserialize(self, value, attr, obj, **kwargs):
        try:
            return timezone(value)
        except Exception as e:
            raise ValidationException("Invalid timezone: {}".format(value))
