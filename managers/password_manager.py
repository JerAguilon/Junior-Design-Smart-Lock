from typing import Dict

from managers.lock_manager import get_lock
from document_templates.lock import Password, PasswordMetadata, PasswordType
from utils.exceptions import AppException, ValidationException
from firebase.firebase_config import DB


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


def get_passwords_metadata(lock_id):
    passwords = get_lock(lock_id).get('passwords', {})

    result = {
        'otp': [],
        'permanent': [],
    }
    for pw_id, password in passwords.items():
        password_type = PasswordType(password['type'])
        if password_type == PasswordType.OTP:
            result['otp'].append(PasswordMetadata.from_database(
                pw_id, password
            ))
        elif password_type == PasswordType.PERMANENT:
            result['permanent'].append(PasswordMetadata.from_database(
                pw_id, password
            ))
        else:
            raise AppException("Error: a password entry is malformed.")
    return result


def add_password(lock_id, password: Password) -> PasswordMetadata:
    new_id = DB.child("Locks").child(lock_id).child("passwords").push(
        password.serialize())['name']
    # return a metadata object instead of a password to ensure that the
    # password is not shared with the outside world
    return PasswordMetadata(password.type, password.expiration, new_id)


def update_password(
    lock_id: str,
    password_id: str,
    update_request: Dict[str, str]
) -> PasswordMetadata:
    if len(update_request.keys()) == 0:
        raise ValidationException("Fields to update weren't supplied")

    DB.child("Locks").child(lock_id).child("passwords").child(
        password_id).update(update_request)
    return get_password_metadata(lock_id, password_id)
