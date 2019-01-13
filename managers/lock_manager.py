from secrets import DB, ID_TOKEN

def create_or_update_lock(lock):
    DB.child("Locks").set(lock.serialize(), ID_TOKEN)

def add_user_lock(user_lock):
    prev_lock_ids = DB.child("UserLocks").child(user_lock.email).get().get('owned_lock_ids')
    user_lock.owned_lock_ids = list(
        set(prev_lock_ids).union(set(user_lock.owned_lock_ids))
    )
    DB.child("UserLocks").set(user_lock.serialize(), ID_TOKEN)

