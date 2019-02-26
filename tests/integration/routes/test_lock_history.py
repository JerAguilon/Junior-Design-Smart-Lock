import pytest

from freezegun import freeze_time
from utils.time_utils import get_current_time_ms

from document_templates.lock import LockStatus
from document_templates.history import StateChange

def _add_password(
        client,
        id_token,
        seeded_user,
        mock_password,
        seeded_lock,
        password_str,
):
    client.post(
        '/api/v1/locks/{}/passwords'.format(seeded_lock.id),
        headers={
            'Authorization': id_token,
        },
        json={
            'password': password_str,
            'type': mock_password.type.value,
            'activeDays': [day.value for day in mock_password.active_days]
        }
    )

@pytest.mark.usefixtures("seeded_user_lock")
def _request_unlock(
    client,
    id_token,
    seeded_user,
    mock_password,
    seeded_lock,
    password_str,
):
    lock_id = seeded_lock.id
    client.put(
        '/api/v1/locks/{}/status'.format(lock_id),
        headers={
            'Authorization': id_token,
        },
        json={
            'status': LockStatus.OPEN_REQUESTED.value,
            'password': password_str
        }
    )

@pytest.mark.usefixtures("seeded_user_lock")
def test_get_history_lock_doesnt_exist(
    client,
    id_token,
    seeded_user,
):
    response = client.get(
        '/api/v1/locks/{}/history'.format(
            'FOOBAR'
        ),
        headers={
            'Authorization': id_token
        }
    )
    expected_json = {
        'error': 'Lock could not be identified'
    }
    assert response.status_code == 401
    assert response.get_json() == expected_json

@pytest.mark.usefixtures("seeded_user_lock")
def test_get_history_empty_history(
    client,
    id_token,
    seeded_user,
    seeded_lock,
):
    response = client.get(
        '/api/v1/locks/{}/history'.format(
            seeded_lock.id
        ),
        headers={
            'Authorization': id_token
        }
    )
    expected_json = {
        'events': []
    }
    assert response.status_code == 200
    assert response.get_json() == expected_json

@pytest.mark.usefixtures("seeded_user_lock")
def test_get_history_with_history(
    client,
    id_token,
    seeded_user,
    mock_password,
    seeded_lock,
    default_password
):
    with freeze_time("August, 1, 2019") as frozen_time:
        # 1. Add a password to for the lock
        _add_password(client, id_token, seeded_user, mock_password, seeded_lock, default_password)
        pw_time = get_current_time_ms()
        frozen_time.tick()

        # 1. Successfully request an unlock
        _request_unlock(client, id_token, seeded_user, mock_password, seeded_lock, default_password)
        unlock_time_success = get_current_time_ms()
        frozen_time.tick()

        # 1. Pass an incorrect password
        _request_unlock(client, id_token, seeded_user, mock_password, seeded_lock, '192168')
        unlock_time_fail = get_current_time_ms()
        frozen_time.tick()

        response = client.get(
            '/api/v1/locks/{}/history'.format(
                seeded_lock.id
            ),
            headers={
                'Authorization': id_token
            }
        )
        expected_json = {
            'events': [
                {
                    'createdAt': pw_time,
                    'endpoint': '/api/v1/locks/<lockId>/passwords',
                    'lockId': seeded_lock.id,
                    'status': StateChange.PASSWORD_CREATED.value,
                    'userId': seeded_user.id,
                },
                {
                    'createdAt': unlock_time_success,
                    'endpoint': '/api/v1/locks/<lockId>/status',
                    'lockId': seeded_lock.id,
                    'status': StateChange.LOCK_STATE_CHANGED.value,
                    'userId': seeded_user.id,
                },
                {
                    'createdAt': unlock_time_fail,
                    'endpoint': '/api/v1/locks/<lockId>/status',
                    'lockId': seeded_lock.id,
                    'status': StateChange.NONE.value,
                    'userId': seeded_user.id,
                },
            ]
        }
        assert response.status_code == 200
        assert response.get_json() == expected_json
