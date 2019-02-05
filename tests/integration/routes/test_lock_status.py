import pytest

from document_templates.lock import LockStatus
from document_templates.password import Password, PasswordType


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
