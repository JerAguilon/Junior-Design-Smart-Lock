from enum import Enum

from utils.time_utils import get_current_time_ms


class StateChange(Enum):
    NONE = "NONE"
    PASSWORD_CREATED = "PASSWORD_CREATED"
    PASSWORD_METADATA_CHANGED = "PASSWORD_METADATA_CHANGED"
    LOCK_METADATA_CHANGED = "LOCK_METADATA_CHANGED"
    LOCK_STATE_CHANGED = "LOCK_STATE_CHANGED"
    USER_LOCK_ADDED = "USER_LOCK_ADDED"


class Event(object):
    def __init__(
        self,
        user_id,
        lock_id,
        endpoint,
        status,
        created_at=None,
        id="UNKNOWN",
    ):
        if not created_at:
            created_at = get_current_time_ms()
        self.user_id = user_id
        self.lock_id = lock_id
        self.endpoint = endpoint
        self.status = status
        self.id = id
        self.created_at = created_at

    def serialize(self):
        return {
            'lockId': self.lock_id,
            'userId': self.user_id,
            'endpoint': self.endpoint,
            'status': self.status.value,
            'createdAt': self.created_at,
        }

    @staticmethod
    def from_database(event_id, d):
        return Event(
            user_id=d['userId'],
            lock_id=d['lockId'],
            endpoint=d['endpoint'],
            status=StateChange(d['status']),
            created_at=d['createdAt'],
            id=event_id,
        )
