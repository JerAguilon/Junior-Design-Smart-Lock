from flask import request, abort

from utils.exceptions import AdminOnlyException

from managers.user_manager import create_or_update_user_from_json
from secrets import AUTH, DB


def authorize(admin=False):
    def actual_decorator(f):
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

            if admin and not found_user.get('is_admin', False):
                raise AdminOnlyException("Admin account required")

            return f(uid, user, *args, **kws)
        return decorated_func
    return actual_decorator
