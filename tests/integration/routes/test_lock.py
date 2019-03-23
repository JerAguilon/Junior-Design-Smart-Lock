def test_delete_lock_unauthorized(client):
    response = client.delete(
        '/api/v1/locks/asdf'
    )
    assert response.status_code == 401
    assert 'message' in response.get_json()


def test_delete_locks_with_id(client, id_token, seeded_user_lock):
    lock_id = seeded_user_lock.owned_lock_ids[0]

    response = client.delete(
        '/api/v1/locks/{}'.format(lock_id),
        headers={
            'Authorization': id_token,
        }
    )
    assert response.status_code == 200
    assert response.get_json() == {'ownedLockIds': []}
