class UserLock(object):
    def __init__(
        self,
        id,
        owned_lock_ids
    ):
        self.id = id
        self.owned_lock_ids = owned_lock_ids

    def serialize(self):
        return {
            "id": self.id,
            "owned_lock_ids": self.owned_lock_ids
        }
