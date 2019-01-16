from secrets import DB
from document_templates.user import User

def create_or_update_user(uid, user):
    DB.child("Users").child(uid).set(user.serialize())

def create_or_update_user_from_json(uid, user):
    create_or_update_user(uid, User(email=user['email'], name=user.get('displayName')))

def create_or_update_user_locks(user_locks):
    DB.child("UserLocks").set(user_locks.serialize())

def get_user(uid):
    return { 'owned_lock_ids' : DB.child("Users").child(uid).get().val() }
