from document_templates.lock import Lock
from managers.lock_manager import add_lock


def test_get_user_lock_unauthorized(client):
    response = client.get('/api/v1/locks')
    assert response.status_code == 401
    assert 'message' in response.get_json()


def test_get_locks_no_locks(client, id_token):
    response = client.get(
        '/api/v1/locks',
        headers={'Authorization': id_token}
    )
    expected_json = {
        'ownedLockIds': []
    }
    assert response.status_code == 200
    assert response.get_json() == expected_json


def test_post_locks_empty(client, id_token):
    response = client.post(
        '/api/v1/locks',
        headers={'Authorization': id_token},
        json={"ownedLockIds": []},
    )
    expected_json = {
        'ownedLockIds': []
    }
    assert response.status_code == 200
    assert response.get_json() == expected_json


def test_post_locks_with_id(client, id_token):
    lock_template = Lock()
    new_id = next(iter(add_lock(lock_template).keys()))
    assert lock_template.id == new_id

    response = client.post(
        '/api/v1/locks',
        headers={'Authorization': id_token},
        json={"ownedLockIds": [new_id]},
    )
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json.keys() == {'ownedLockIds'}
    assert response_json['ownedLockIds'] == [new_id]
