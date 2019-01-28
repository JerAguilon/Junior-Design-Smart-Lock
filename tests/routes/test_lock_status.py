import pytest

from document_templates.lock import LockStatus
from security.security_utils import verify_password


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
def test_put_lock_status_open_requested_correct_password(
        client, id_token, seeded_lock, seeded_user, db, mocker):
    password_check = mocker.patch(
        'security.security_utils.verify_password', return_value=None)

    lock_id = seeded_lock.id
    response = client.put(
        '/api/v1/locks/{}/status'.format(lock_id),
        headers={
            'Authorization': id_token,
        },
        json={
            'status': LockStatus.OPEN_REQUESTED.value,
            'password': '123456'
        }
    )
    assert response.status_code == 200
    assert response.get_json() == {'status': LockStatus.OPEN_REQUESTED.value}
    password_check.assert_called_once_with(lock_id, '123456')


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
