from secrets import DB

def add_lock(lock):
    new_id = DB.push().key()
    result = DB.child("Locks").child(new_id).set(lock.serialize())
    return { new_id : result.get().val() }

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
