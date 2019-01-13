class UserLock(object):
    def __init__(
        self,
        email,
        owned_lock_ids
    ):
        self.email = email
        self.owned_lock_ids = owned_lock_ids

    def serialize(self):
        return {
            "email": self.email,
            "owned_lock_ids": self.owned_lock_ids,
        }
