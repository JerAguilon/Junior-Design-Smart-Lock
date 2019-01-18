from secrets import *
from utils.exceptions import AuthorizationException


def verify_lock_ownership(uid, lock_id):
    is_owned = True
    error_message = ''

    uid_lookup = DB.child("UserLocks").child(uid).get().val()

    if DB.child("Locks").child(lock_id).get().val() is None:
        is_owned = False
        message = 'Lock could not be identified'
    elif uid_lookup is None:
        is_owned = False
        message = 'User could not be identified'
    else:
        owned_locks = set(uid_lookup.get('ownedLockIds'))
        if lock_id not in owned_locks:
            is_owned = False
            message = 'User does not own this lock'

    if not is_owned:
        raise AuthorizationException(message=message)
