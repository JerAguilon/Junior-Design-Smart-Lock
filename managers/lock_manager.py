from secrets import DB
from document_templates.lock import LockStatus
from utils.exceptions import AuthorizationException, ValidationException


def add_lock(lock):
    new_id = DB.child("Locks").push(lock.serialize())['name']
    return { new_id : lock.serialize() }


def get_locks(lock_ids):
    return {
        lock_id: DB.child("Locks").child(lock_id).get().val() for lock_id in lock_ids
    }

def get_lock(lock_id):
    return get_locks([lock_id])[lock_id]

def change_lock_status(lock_id, status):
    DB.child("Locks").child(lock_id).update({ 'status': status.value })
    return {
        "lockStatus": status.value
    }

def get_lock_status(lock_id):
    status_str = DB.child("Locks").child(lock_id).get().val().get("status")
    return {
        "lockStatus": status_str
    }

