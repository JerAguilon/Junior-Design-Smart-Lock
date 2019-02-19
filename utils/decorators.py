import base64

from flask import request, abort
from functools import wraps

from utils.exceptions import AuthorizationException, AdminOnlyException, ValidationException

from managers.user_manager import create_or_update_user_from_json
from firebase.firebase_config import AUTH, DB
from security import security_utils


def authorize_hardware():
    def actual_decorator(f):
        @wraps(f)
        def decorated_func(*args, **kws):
            if 'Authorization' in request.headers:
                header_key = 'Authorization'
            else:
                abort(401)
            data = str(request.headers[header_key])

            if not data.startswith('Basic'):
                raise ValidationException("Basic authorization required")

            coded_string = str.replace(str(data), 'Basic ', '')
            decoded = base64.b64decode(coded_string).decode('utf-8')
            string_split = decoded.split(':')
            if len(string_split) < 2:
                raise AuthorizationException(
                    "Basic auth must be base-64 encoded in 'lockId:password' format")

            lock_id, secret = string_split[0], ':'.join(string_split[1:])
            try:
                secret_hashed = DB.child("Locks").child(
                    lock_id).get().val().get('secret')
            except BaseException:
                raise AuthorizationException("Lock could not be found")

            if not security_utils.check_password(secret, secret_hashed):
                raise AuthorizationException("Invalid secret supplied")
            return f(lock_id, *args, **kws)
        return decorated_func
    return actual_decorator


def authorize(admin=False):
    def actual_decorator(f):
        @wraps(f)
        def decorated_func(*args, **kws):
            if 'api_key' in request.args:
                token = request.args['api_key']
            else:
                if 'Authorization' in request.headers:
                    header_key = 'Authorization'
                elif 'Api-Key' in request.headers:
                    header_key = 'Api-Key'
                else:
                    abort(401)
                data = str(request.headers[header_key])
                token = str.replace(str(data), 'Bearer ', '')

            try:
                user = AUTH.get_account_info(token)['users'][0]
            except BaseException:
                abort(401)
            uid = user['localId']
            found_user = DB.child("Users").child(uid).get().val()
            if not found_user:
                create_or_update_user_from_json(uid, user)

            if admin and not found_user.get('isAdmin', False):
                raise AdminOnlyException("Admin account required")

            return f(uid, user, *args, **kws)
        return decorated_func
    return actual_decorator


def use_request_form(required_fields=[]):
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
                    "Missing arguments, required fields: {}".format(
                        required_fields
                    )
                )
            return function(request_form, *args, **kwargs)
        return wrapper
    return actual_decorator
