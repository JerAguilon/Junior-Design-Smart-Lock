from typing import Optional

import bcrypt

from firebase.firebase_config import DB
from utils.exceptions import AuthorizationException, ValidationException
from document_templates.password import PasswordType, Password


def _get_sorted_passwords(lock_id):
    type_ordinal = {
        PasswordType.PERMANENT: 0,
        PasswordType.OTP: 1,
    }

    passwords = DB.child("Locks").child(lock_id).child("passwords").get().val()
    passwords_list = [
        (pw_id, password_dict) for pw_id, password_dict in passwords.items()
    ]
    passwords_list = sorted(
        passwords_list,
        key=lambda x: type_ordinal[PasswordType(x[1]['type'])]
    )
    return [
        Password(
            type=PasswordType(password_dict['type']),
            password=password_dict['password'],
            expiration=password_dict['expiration'],
            id=id
        ) for id, password_dict in passwords_list
    ]


def hash_password(plaintext):
    if isinstance(plaintext, str):
        plaintext = bytes(plaintext, 'utf-8')
    return str(bcrypt.hashpw(plaintext, bcrypt.gensalt()), 'utf8')


def check_password(plaintext, hashed):
    if isinstance(plaintext, str):
        plaintext = bytes(plaintext, 'utf-8')
    if isinstance(hashed, str):
        hashed = bytes(hashed, 'utf-8')
    return bcrypt.checkpw(plaintext, hashed)


def verify_lock_ownership(uid, lock_id):
    is_owned = True
    message = ''

    uid_lookup = DB.child("UserLocks").child(uid).get().val()

    if DB.child("Locks").child(lock_id).get().val() is None:
        is_owned = False
        message = 'Lock could not be identified'
    elif uid_lookup is None:
        is_owned = False
        message = 'User could not be identified or has not registered a lock'
    else:
        owned_locks = set(uid_lookup.get('ownedLockIds'))
        if lock_id not in owned_locks:
            is_owned = False
            message = 'User does not own this lock'

    if not is_owned:
        raise AuthorizationException(message=message)


def verify_password(lock_id, input_password: Optional[str]) -> Password:
    if input_password is None:
        raise ValidationException("A password must be supplied")

    passwords_list = _get_sorted_passwords(lock_id)

    for password in passwords_list:
        if check_password(input_password, password.hashed_password):
            return password
    raise AuthorizationException("Invalid password supplied")
