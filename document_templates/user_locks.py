from document_templates.template_utils import require_fields


class UserLocks(object):
    def __init__(
        self,
        owned_lock_ids
    ):
        self.owned_lock_ids = owned_lock_ids

    def serialize(self):
        return {
            'ownedLockIds': self.owned_lock_ids
        }

    @staticmethod
    @require_fields(['ownedLockIds'])
    def build(request_form):
        return UserLocks(
            owned_lock_ids=request_form['ownedLockIds']
        )
