from typing import Dict

from managers.lock_manager import get_lock
from document_templates.password import (
    Password, PasswordMetadata, PasswordType
)
from utils.exceptions import AppException, ValidationException
from firebase.firebase_config import DB


def _get_password_from_db(lock_id, password_id):
    passwords = get_lock(lock_id).get('passwords', {})

    for pw_id, found_password in passwords.items():
        if pw_id == password_id:
            return found_password
    raise ValidationException(
        "Password id could not be found belonging to the lock id")


def get_password_metadata(lock_id, password_id):
    found_password = _get_password_from_db(lock_id, password_id)
    if found_password:
        return PasswordMetadata.from_database(password_id, found_password)


def get_password(lock_id, password_id):
    found_password = _get_password_from_db(lock_id, password_id)
    if found_password:
        return Password.from_database(password_id, found_password)


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
        elif password_type == PasswordType.UNLIMITED:
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
    return PasswordMetadata(
        type=password.type,
        expiration=password.expiration,
        active_days=password.active_days,
        active_times=password.active_times,
        id=new_id,
    )


def remove_password(lock_id: str, password: Password) -> None:
    remove_password_by_id(lock_id, password.id)


def remove_password_by_id(lock_id: str, password_id: str) -> None:
    DB.child("Locks").child(lock_id).child("passwords").child(
        password_id
    ).remove()


def update_password(
    lock_id: str,
    password_id: str,
    update_request: Dict[str, str]
) -> PasswordMetadata:
    if len(update_request.keys()) == 0:
        raise ValidationException("Fields to update weren't supplied")
    password = get_password(lock_id, password_id)
    password.update(update_request)

    DB.child("Locks").child(lock_id).child("passwords").child(
        password_id).update(password.serialize())
    return get_password_metadata(lock_id, password_id)
