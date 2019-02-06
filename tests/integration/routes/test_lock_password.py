import pytest

from document_templates.password import PasswordType
from security.security_utils import check_password


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
        'activeDays': [d.value for d in seeded_password.active_days],
    }
    assert response.status_code == 200
    assert response.get_json() == expected_json


@pytest.mark.usefixtures("seeded_user_lock")
def test_put_password_no_updates(
    client,
    id_token,
    seeded_user,
    seeded_lock,
    seeded_password
):
    response = client.put(
        '/api/v1/locks/{}/passwords/{}'.format(
            seeded_lock.id, seeded_password.id
        ),
        headers={
            'Authorization': id_token
        },
        json={
        }
    )
    assert response.status_code == 422
    assert response.get_json() == {
        'error': 'Fields to update weren\'t supplied'
    }


@pytest.mark.usefixtures("seeded_user_lock")
def test_put_password(
    db,
    client,
    id_token,
    seeded_user,
    seeded_lock,
    seeded_password
):
    password_plaintext = '162515'
    response = client.put(
        '/api/v1/locks/{}/passwords/{}'.format(
            seeded_lock.id, seeded_password.id
        ),
        headers={
            'Authorization': id_token
        },
        json={
            'password': password_plaintext,
            'activeDays': ['MONDAY']
        }
    )

    expected_json = {
        'id': seeded_password.id,
        'type': seeded_password.type.value,
        'createdAt': seeded_password.created_at,
        'activeDays': ['MONDAY'],
        'expiration': -1,
    }
    assert response.status_code == 200
    assert response.get_json() == expected_json
    new_password = db.child("Locks").child(seeded_lock.id).child(
        "passwords").child(seeded_password.id).get().val()['password']
    assert check_password(password_plaintext, new_password)
