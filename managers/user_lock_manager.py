from secrets import DB

def create_or_update_user_lock(uid, user_lock, should_overwrite=False):
    if not should_overwrite:
        prev_locks = DB.child("UserLocks").child(uid).get().val().get('owned_lock_ids') or []
        combined_locks = list( set(prev_locks).update(user_lock.owned_lock_ids) )
        user_lock.owned_lock_ids = combined_locks
    DB.child("UserLocks").child(uid).set(user_lock.serialize())
