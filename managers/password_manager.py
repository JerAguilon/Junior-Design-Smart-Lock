from managers.lock_manager import get_lock
from document_templates.lock import Password, PasswordMetadata
from utils.exceptions import ValidationException
from secrets import DB

def get_password_metadata(lock_id, password_id):
    passwords = get_lock(lock_id).get('passwords', {})

    found_password = None
    for pw_id, found_password in passwords.items():
        if pw_id == password_id:
            found_password = found_password

    if found_password:
        return PasswordMetadata.from_database(pw_id, found_password)
    else:
        raise ValidationException(
            "Password id could not be found belonging to the lock id")

def add_password(lock_id, password: Password) -> PasswordMetadata:
    new_id = DB.child("Locks").child(lock_id).child("passwords").push(
        password.serialize())['name']
    # return a metadata object instead of a password to ensure that the
    # password is not shared with the outside world
    return PasswordMetadata(password.type, password.expiration, new_id)
