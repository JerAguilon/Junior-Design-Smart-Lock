from utils.exceptions import ValidationException
from firebase.firebase_config import DB


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


def delete_user_lock(uid, lock_id):
    user_lock_entry = DB.child("UserLocks").child(uid).get().val()

    owned_locks = set(user_lock_entry.get(
        'ownedLockIds') if user_lock_entry else [])
    owned_locks.remove(lock_id)

    DB.child("UserLocks").child(uid).set(list(owned_locks))

    # TODO: more expensive than necessary, can simply build
    # an object using the variables above
    return get_user_locks(uid)


def get_user_locks(uid):
    owned_lock_ids = DB.child("UserLocks").child(
        uid).child('ownedLockIds').get().val()
    if owned_lock_ids is None:
        owned_lock_ids = []
    return {'ownedLockIds': owned_lock_ids}
