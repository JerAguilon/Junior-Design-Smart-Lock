from utils.exceptions import ValidationException

def require_fields(required_fields=[]):
    def actual_decorator(function):
        def wrapper(*args, **kwargs):
            request_form = args[0]
            is_valid = all(f in request_form for f in required_fields)
            if not is_valid:
                raise ValidationException("Missing arguments, required fields: {}".format(required_fields))
            return function(*args, **kwargs)
        return wrapper
    return actual_decorator
