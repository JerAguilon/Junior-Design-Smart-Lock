class UserLocks(object):
    def __init__(
        self,
        owned_lock_ids
    ):
        self.owned_lock_ids = owned_lock_ids

    def serialize(self):
        return {
            'owned_lock_ids': self.owned_lock_ids
        }
