from utils.exceptions import ValidationException
from secrets import DB


def create_or_update_user_lock(uid, user_locks, should_overwrite=False):
    invalid_ids = []
    for lock_id in user_locks.owned_lock_ids:
        if DB.child("Locks").child(lock_id).get().val() is None:
            invalid_ids.append(lock_id)

    if len(invalid_ids) > 0:
        raise ValidationException("Invalid lock ids: {}".format(invalid_ids))

    if not should_overwrite:
        user_lock_entry = DB.child("UserLocks").child(uid).get().val()
        prev_locks = user_lock_entry.get(
            'ownedLockIds') if user_lock_entry else []

        combined_locks = list(set(prev_locks).union(user_locks.owned_lock_ids))
        user_locks.owned_lock_ids = combined_locks
    DB.child("UserLocks").child(uid).set(user_locks.serialize())
    return user_locks.serialize()


def get_user_locks(uid):
    return {'ownedLockIds': DB.child("UserLocks").child(uid).child('ownedLockIds').get().val()}
