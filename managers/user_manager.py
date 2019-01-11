from secrets import DB, ID_TOKEN

def create_or_update_user(user):
    DB.child("Users").set(user.serialize(), ID_TOKEN)

def create_or_update_user_locks(user_locks):
    DB.child("UserLocks").set(user_locks.serialize(), ID_TOKEN)
