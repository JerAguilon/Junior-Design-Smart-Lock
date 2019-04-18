import pytest

from freezegun import freeze_time

from document_templates.lock import LockStatus
from document_templates.password import Password, PasswordType, PasswordDays
from utils import time_utils


def test_get_lock_status_unauthorized(client, id_token):
    response = client.get('/api/v1/locks/foobar/status')
    assert response.status_code == 401
    assert 'message' in response.get_json()


@pytest.mark.usefixtures("seeded_user_lock", "seeded_user")
def test_get_lock_status(client, id_token, seeded_lock, db):
    lock_id = seeded_lock.id
    response = client.get(
        '/api/v1/locks/{}/status'.format(lock_id),
        headers={
            'Authorization': id_token,
        }
    )
    assert response.status_code == 200
    assert response.get_json() == {'status': 'CLOSED'}


@pytest.mark.usefixtures("seeded_user")
def test_get_lock_status_not_owned(client, id_token, seeded_lock, db):
    lock_id = seeded_lock.id
    response = client.get(
        '/api/v1/locks/{}/status'.format(lock_id),
        headers={
            'Authorization': id_token,
        }
    )
    assert response.status_code == 401
    assert response.get_json() == {
        'error': 'User could not be identified or has not registered a lock'}


@pytest.mark.usefixtures("seeded_user")
def test_put_lock_status_not_owned(client, id_token, seeded_lock, db):
    lock_id = seeded_lock.id
    response = client.put(
        '/api/v1/locks/{}/status'.format(lock_id),
        headers={
            'Authorization': id_token,
        },
        json={
            'status': LockStatus.OPEN_REQUESTED.value
        }
    )
    assert response.status_code == 401
    assert response.get_json() == {
        'error': 'User could not be identified or has not registered a lock'}


@pytest.mark.usefixtures("seeded_user_lock")
def test_put_lock_status_open_requested_correct_password_permanent(
    client,
    id_token,
    get_mock_password,
    seeded_lock,
    seeded_user,
    seeded_password,
    db,
    mocker
):
    lock_id = seeded_lock.id
    response = client.put(
        '/api/v1/locks/{}/status'.format(lock_id),
        headers={
            'Authorization': id_token,
        },
        json={
            'status': LockStatus.OPEN_REQUESTED.value,
            'password': get_mock_password()
        }
    )
    assert response.status_code == 200
    assert response.get_json() == {
        'status': LockStatus.OPEN_REQUESTED.value,
        'providedPasswordDisabled': False
    }


@pytest.mark.usefixtures("seeded_user", "seeded_user_lock")
def test_put_lock_status_open_requested_correct_password_otp(
    client,
    id_token,
    seeded_lock,
    seeded_password,  # A permanent password
    seed_password,
    get_mock_password,
    db,
    mocker
):
    pw_str = "192168"
    otp_password = Password(
        type=PasswordType.OTP,
        password=get_mock_password(pw_str, hashed=True)
    )
    otp_password = seed_password(password=otp_password, lock=seeded_lock)

    lock_id = seeded_lock.id
    response = client.put(
        '/api/v1/locks/{}/status'.format(lock_id),
        headers={
            'Authorization': id_token,
        },
        json={
            'status': LockStatus.OPEN_REQUESTED.value,
            'password': pw_str
        }
    )
    active_password_keys = db.child('Locks').child(lock_id).child(
        'passwords').get().val().keys()
    assert otp_password.id not in active_password_keys
    assert response.status_code == 200
    assert response.get_json() == {
        'status': LockStatus.OPEN_REQUESTED.value,
        'providedPasswordDisabled': True
    }


@pytest.mark.usefixtures("seeded_user", "seeded_user_lock")
def test_put_lock_status_other_status(client, id_token, seeded_lock, db):
    lock_id = seeded_lock.id
    for status in [LockStatus.CLOSED, LockStatus.OPEN]:
        response = client.put(
            '/api/v1/locks/{}/status'.format(lock_id),
            headers={
                'Authorization': id_token,
            },
            json={
                'status': status.value
            }
        )
        expected_message = 'Users cannot set the lock to open or closed. ' + \
            'Open or close the vault to do so.'

        assert response.status_code == 401
        assert response.get_json() == {
            'error': expected_message
        }


@pytest.mark.usefixtures("seeded_user", "seeded_user_lock")
def test_put_lock_status_open_requested_expired_password(
    client,
    id_token,
    seeded_lock,
    seeded_password,  # A permanent password
    seed_password,
    get_mock_password,
    db,
    mocker
):
    with freeze_time("Feb 2nd, 2019") as frozen_time:
        pw_str = "192168"
        expired_pw = Password(
            type=PasswordType.UNLIMITED,
            expiration=time_utils.get_current_time_ms(),
            password=get_mock_password(pw_str, hashed=True)
        )
        expired_pw = seed_password(password=expired_pw, lock=seeded_lock)
        frozen_time.tick()

        lock_id = seeded_lock.id
        response = client.put(
            '/api/v1/locks/{}/status'.format(lock_id),
            headers={
                'Authorization': id_token,
            },
            json={
                'status': LockStatus.OPEN_REQUESTED.value,
                'password': pw_str
            }
        )

        assert response.status_code == 401
        assert response.get_json() == {
            "error": "Invalid or inactive password supplied"
        }

        # Expired passwords should be removed from the database
        # after PUT request
        active_password_keys = db.child('Locks').child(lock_id).child(
            'passwords').get().val().keys()
        assert expired_pw.id not in active_password_keys
        assert seeded_password.id in active_password_keys


@pytest.mark.usefixtures("seeded_user", "seeded_user_lock")
def test_put_lock_status_open_requested_password_not_active_day(
    client,
    id_token,
    seeded_lock,
    seeded_password,  # A permanent password
    seed_password,
    get_mock_password,
    db,
    mocker
):
    # Feb 11 2019 is a Monday
    # NOTE: the lock is located in eastern time, GMT-5
    # (see document_templates.Lock.timezone)
    with freeze_time("Feb 11th, 2019 23:59:59", tz_offset=0):
        pw_str = "192168"
        expired_pw = Password(
            type=PasswordType.UNLIMITED,
            active_days=[PasswordDays.MONDAY],
            password=get_mock_password(pw_str, hashed=True)
        )
        expired_pw = seed_password(password=expired_pw, lock=seeded_lock)

    # One second before Tuesday in eastern time
    with freeze_time("Feb 12th, 2019 04:59:59", tz_offset=0):
        lock_id = seeded_lock.id
        response = client.put(
            '/api/v1/locks/{}/status'.format(lock_id),
            headers={
                'Authorization': id_token,
            },
            json={
                'status': LockStatus.OPEN_REQUESTED.value,
                'password': pw_str
            }
        )
        assert response.status_code == 200

    # Exactly on Tuesday
    with freeze_time("Feb 12th, 2019 05:00:00", tz_offset=0):
        lock_id = seeded_lock.id
        response = client.put(
            '/api/v1/locks/{}/status'.format(lock_id),
            headers={
                'Authorization': id_token,
            },
            json={
                'status': LockStatus.OPEN_REQUESTED.value,
                'password': pw_str
            }
        )
        assert response.status_code == 401
        assert response.get_json() == {
            "error": "Invalid or inactive password supplied"
        }

        # Expired passwords should be removed from the database
        # after PUT request
        active_password_keys = db.child('Locks').child(lock_id).child(
            'passwords').get().val().keys()

        # Both passwords should be in the DB still
        assert expired_pw.id in active_password_keys
        assert seeded_password.id in active_password_keys


@pytest.mark.usefixtures("seeded_user", "seeded_user_lock")
def test_put_lock_status_open_requested_password_not_active_time(
    client,
    id_token,
    seeded_lock,
    seeded_password,  # A permanent password
    seed_password,
    get_mock_password,
    db,
    mocker
):
    # Feb 11 2019 is a Monday
    # NOTE: the lock is located in eastern time, GMT-5
    # (see document_templates.Lock.timezone)
    with freeze_time("Feb 11th, 2019 17:59:59", tz_offset=0):
        pw_str = "192168"
        expired_pw = Password(
            type=PasswordType.UNLIMITED,
            active_days=[PasswordDays.MONDAY],
            active_times=['12:00', '13:00'],
            password=get_mock_password(pw_str, hashed=True)
        )
        expired_pw = seed_password(password=expired_pw, lock=seeded_lock)

        lock_id = seeded_lock.id
        response = client.put(
            '/api/v1/locks/{}/status'.format(lock_id),
            headers={
                'Authorization': id_token,
            },
            json={
                'status': LockStatus.OPEN_REQUESTED.value,
                'password': pw_str
            }
        )
        assert response.status_code == 200

    # One second past the expiration time (13:00:01 ET)
    with freeze_time("Feb 11th, 2019 18:00:01", tz_offset=0):
        lock_id = seeded_lock.id
        response = client.put(
            '/api/v1/locks/{}/status'.format(lock_id),
            headers={
                'Authorization': id_token,
            },
            json={
                'status': LockStatus.OPEN_REQUESTED.value,
                'password': pw_str
            }
        )
        assert response.status_code == 401
        assert response.get_json() == {
            "error": "Invalid or inactive password supplied"
        }

        # Expired passwords should be removed from the database
        # after PUT request
        active_password_keys = db.child('Locks').child(lock_id).child(
            'passwords').get().val().keys()

        # Both passwords should be in the DB still
        assert expired_pw.id in active_password_keys
        assert seeded_password.id in active_password_keys


@pytest.mark.usefixtures("seeded_user", "seeded_user_lock")
def test_put_lock_status_open_requested_no_registered_passwords(
    client,
    id_token,
    seeded_lock,
    get_mock_password,
    db,
    mocker
):
    pw_str = "192168"

    lock_id = seeded_lock.id
    response = client.put(
        '/api/v1/locks/{}/status'.format(lock_id),
        headers={
            'Authorization': id_token,
        },
        json={
            'status': LockStatus.OPEN_REQUESTED.value,
            'password': pw_str
        }
    )

    assert response.status_code == 401
    assert response.get_json() == {
        "error": "Invalid or inactive password supplied"
    }
