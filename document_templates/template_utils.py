from flask import request

from utils.exceptions import ValidationException
from functools import wraps


def require_fields(required_fields=[]):
    def actual_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            request_form = request.form.to_dict()
            if len(request_form) == 0 and request.get_json() and len(
                    request.get_json()) > 0:
                request_form = request.get_json()
            is_valid = all(f in request_form for f in required_fields)
            if not is_valid:
                raise ValidationException(
                    "Missing arguments, required fields: {}".format(required_fields))
            return function(request_form, **kwargs)
        return wrapper
    return actual_decorator
