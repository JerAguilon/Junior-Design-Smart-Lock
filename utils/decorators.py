from flask import request, abort

from utils.exceptions import ValidationException
from functools import wraps

from document_templates.user import User
from managers.user_manager import create_or_update_user
from secrets import AUTH, DB

def require_fields(required_fields=[]):
    def actual_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            request_form = request.form.to_dict()
            if len(request_form) == 0 and len(request.get_json()) > 0:
                request_form = request.get_json()
            is_valid = all(f in request_form for f in required_fields)
            if not is_valid:
                raise ValidationException("Missing arguments, required fields: {}".format(required_fields))
            return function(request_form, **kwargs)
        return wrapper
    return actual_decorator

def authorize(f):
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
        if not DB.child("Users").child(uid).get().val():
            create_or_update_user(
                uid, User(email=user['email'], name=user.get('displayName'))
            )
        return f(uid, user, *args, **kws)
    return decorated_func

