import pytest


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
