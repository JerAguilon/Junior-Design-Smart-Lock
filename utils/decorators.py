from flask import request, abort
from functools import wraps

from utils.exceptions import AdminOnlyException

from managers.user_manager import create_or_update_user_from_json
from secrets import AUTH, DB


def authorize(admin=False):
    def actual_decorator(f):
        @wraps(f)
        def decorated_func(*args, **kws):
            if not 'Authorization' in request.headers:
                abort(401)
            data = str(request.headers['Authorization'])
            token = str.replace(str(data), 'Bearer ', '')
            try:
                user = AUTH.get_account_info(token)['users'][0]
            except:
                abort(401)
            uid = user['localId']
            found_user = DB.child("Users").child(uid).get().val()
            if not found_user:
                create_or_update_user_from_json(uid, user)

            if admin and not found_user.get('isAdmin', False):
                raise AdminOnlyException("Admin account required")

            return f(uid, user, *args)
        return decorated_func
    return actual_decorator

def use_request_form(required_fields=[]):
    def actual_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            request_form = request.form.to_dict()
            if len(request_form) == 0 and request.get_json() and len(request.get_json()) > 0:
                request_form = request.get_json()
            is_valid = all(f in request_form for f in required_fields)
            if not is_valid:
                raise ValidationException("Missing arguments, required fields: {}".format(required_fields))
            return function(request_form, *args, **kwargs)
        return wrapper
    return actual_decorator
