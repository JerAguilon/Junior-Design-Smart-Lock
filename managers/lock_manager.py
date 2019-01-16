from secrets import DB

def create_or_update_lock(lock):
    DB.child("Locks").set(lock.serialize())

def add_user_lock(uid, user_lock):
    prev_lock_ids = DB.child("UserLocks").child(user_lock.email).get().get('owned_lock_ids')
    user_lock.owned_lock_ids = list(
        set(prev_lock_ids).union(set(user_lock.owned_lock_ids))
    )
    DB.child("UserLocks").child(uid).set(user_lock.serialize())

def add_lock(lock_id, lock):
    DB.child("Locks").child(lock_id).set(lock.serialize())

def change_lock_status(lock_id, status):
    DB.child("Locks").child(lock_id).child("status").set(status.value)

def get_user_lock(uid):
    return DB.child("UserLocks").child(uid).child('owned_lock_ids').get().val()

def get_locks(lock_ids):
    return {
        lock_id: DB.child("Locks").child(lock_id).get().val() for lock_id in lock_ids
    }

def get_lock(lock_id):
    return get_locks([lock_id])[lock_id]
