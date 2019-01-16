from secrets import DB

def add_lock(lock):
    new_id = DB.child("Locks").push(lock.serialize())['name']
    return { new_id : lock.serialize() }

def change_lock_status(lock_id, status):
    DB.child("Locks").child(lock_id).child("status").set(status.value)

def get_locks(lock_ids):
    return {
        lock_id: DB.child("Locks").child(lock_id).get().val() for lock_id in lock_ids
    }

def get_lock(lock_id):
    return get_locks([lock_id])[lock_id]
