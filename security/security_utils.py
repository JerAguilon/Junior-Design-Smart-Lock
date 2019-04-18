import bcrypt
import datetime

from pytz import timezone
from typing import Optional

from firebase.firebase_config import DB
from utils.exceptions import AuthorizationException, ValidationException
from utils import time_utils
from document_templates.password import PasswordType, Password, PasswordDays


def _prune_passwords(lock_id, passwords):
    for password in passwords:
        DB.child("Locks").child(lock_id).child("passwords").child(
            password.id
        ).remove()


def _password_is_active(password: Password, timezone=timezone("US/Eastern")):
    is_active = True

    if password.active_days != []:
        day = PasswordDays(time_utils.get_current_day(timezone))
        is_active = day in password.active_days

    if password.active_times != []:
        start, end = map(str, password.active_times)
        start_h, start_m = map(int, start.split(':'))
        end_h, end_m = map(int, end.split(':'))

        begin_time = datetime.time(start_h, start_m)
        end_time = datetime.time(end_h, end_m)

        is_active = time_utils.is_time_between(
            begin_time, end_time, timezone=timezone)

    return is_active


def _get_sorted_passwords(lock_id):
    type_ordinal = {
        PasswordType.UNLIMITED: 0,
        PasswordType.OTP: 1,
    }

    passwords = DB.child("Locks").child(
        lock_id).child("passwords").get().val() or {}
    passwords_list = [
        (pw_id, password_dict) for pw_id, password_dict in passwords.items()
    ]
    passwords_list = sorted(
        passwords_list,
        key=lambda x: type_ordinal[PasswordType(x[1]['type'])]
    )
    passwords_list = [
        Password.from_database(id, password_dict)
        for id, password_dict in passwords_list
    ]

    expired_passwords = []
    output = []
    for password in passwords_list:
        if password.expiration != -1 \
                and password.expiration < time_utils.get_current_time_ms():
            expired_passwords.append(password)
        elif _password_is_active(password):
            output.append(password)

    _prune_passwords(lock_id, expired_passwords)
    return output


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
    raise AuthorizationException("Invalid or inactive password supplied")
