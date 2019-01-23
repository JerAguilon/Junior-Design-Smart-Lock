from typing import Optional

import bcrypt

from secrets import DB
from utils.exceptions import AuthorizationException, ValidationException
from document_templates.lock import PasswordType


def hash_password(plaintext):
    if isinstance(plaintext, str):
        plaintext = bytes(plaintext, 'utf-8')
    return str(bcrypt.hashpw(plaintext, bcrypt.gensalt()), 'utf8')


def check_password(plaintext, hashed):
    if isinstance(plaintext, str):
        plaintext = bytes(plaintext, 'utf-8')
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
        message = 'User could not be identified'
    else:
        owned_locks = set(uid_lookup.get('ownedLockIds'))
        if lock_id not in owned_locks:
            is_owned = False
            message = 'User does not own this lock'

    if not is_owned:
        raise AuthorizationException(message=message)


def verify_password(lock_id, input_password: Optional[str]):
    if input_password is None:
        raise ValidationException("A password must be supplied")

    type_ordinal = {
        PasswordType.PERMANENT: 0,
        PasswordType.OTP: 1,
    }

    passwords = DB.child("Locks").child(lock_id).child("passwords").get().val()

    passwords_list = sorted(
        passwords.values(),
        key=lambda x: type_ordinal[PasswordType(x['type'])],
    )
    for password in passwords_list:
        if check_password(input_password, password['password']):
            return
    raise AuthorizationException("Invalid password supplied")
