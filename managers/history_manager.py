from typing import List

from document_templates.history import Event
from firebase.firebase_config import DB


def add_event(event: Event):
    serialized_event = event.serialize()
    new_id = DB.child("EventHistory").push(serialized_event)['name']
    event.id = new_id
    DB.child("LockEvents").child(event.lock_id).set({new_id: True})
    return {new_id: serialized_event}


def get_events_from_lock_id(lock_id: str) -> List[Event]:
    event_ids = DB.child("LockEvents").child(lock_id).get().val().keys()

    output = []
    for event_id in event_ids:
        event = Event.from_database(
            event_id,
            DB.child("EventHistory").child(event_id).get().val()
        )
        output.append(event)
    return output
