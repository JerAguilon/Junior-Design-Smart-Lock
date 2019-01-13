from secrets import DB, ID_TOKEN

from utils import hexify

def create_or_update_user(user):
    DB.child("Users").child(hexify.hexify(user.email)).set(user.serialize(), ID_TOKEN)

def create_or_update_user_locks(user_locks):
    DB.child("UserLocks").set(user_locks.serialize(), ID_TOKEN)
