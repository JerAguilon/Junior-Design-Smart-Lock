from firebase.firebase_config import DB


def add_lock(lock):
    new_id = DB.child("Locks").push(lock.serialize())['name']
    lock.id = new_id
    return {new_id: lock.serialize()}


def get_locks(lock_ids):
    return {
        lock_id: DB.child("Locks").child(lock_id).get().val()
        for lock_id in lock_ids
    }


def get_lock(lock_id):
    return get_locks([lock_id])[lock_id]


def change_lock_status(lock_id, status, was_lock_removed):
    DB.child("Locks").child(lock_id).update({'status': status.value})
    return {
        "status": status.value,
        "inputedPasswordDisabled": was_lock_removed
    }


def get_lock_status(lock_id):
    status_str = DB.child("Locks").child(lock_id).get().val().get("status")
    return {
        "status": status_str
    }
