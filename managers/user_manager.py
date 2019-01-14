from secrets import DB

def create_or_update_user(uid, user):
    DB.child("Users").child(uid).set(user.serialize())

def create_or_update_user_locks(user_locks):
    DB.child("UserLocks").set(user_locks.serialize())
