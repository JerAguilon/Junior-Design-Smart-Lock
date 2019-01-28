import pytest


def test_password_unauthorized(client):
    response = client.get('/api/v1/locks/foobar/passwords/foobaz')
    assert response.status_code == 401
    assert 'message' in response.get_json()


@pytest.mark.usefixtures("seeded_user_lock")
def test_get_password(
    client,
    id_token,
    seeded_user,
    seeded_lock,
    seeded_password
):
    response = client.get(
        '/api/v1/locks/{}/passwords/{}'.format(
            seeded_lock.id, seeded_password.id
        ),
        headers={
            'Authorization': id_token
        }
    )
    expected_json = {
        'createdAt': seeded_password.created_at,
        'expiration': seeded_password.expiration,
        'id': seeded_password.id,
        'type': seeded_password.type.value,
    }
    assert response.status_code == 200
    assert response.get_json() == expected_json
