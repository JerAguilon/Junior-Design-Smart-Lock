import datetime
import pytest

from freezegun import freeze_time

from document_templates.password import PasswordType
from document_templates.lock import LockStatus
from security.security_utils import check_password


def test_post_lock_unauthorized(client):
    response = client.post('/api/v1/admin/locks')
    assert response.status_code == 401
    assert 'message' in response.get_json()


@freeze_time("August, 1, 2019")
def test_post_lock_not_admin(
    client,
    id_token,
    seeded_user,
    mock_lock
):
    response = client.post(
        '/api/v1/admin/locks',
        headers={
            'Authorization': id_token,
        },
        json={
        }
    )
    expected_json = {
        'error': 'Admin account required',
    }
    response_json = response.get_json()
    assert response.status_code == 401
    assert response_json == expected_json


@freeze_time("August, 1, 2019")
def test_post_lock_no_args_admin(
    client,
    id_token,
    seeded_admin_user,
):
    response = client.post(
        '/api/v1/admin/locks',
        headers={
            'Authorization': id_token,
        },
        json={
        }
    )
    expected_json = {
        'status': LockStatus.CLOSED.value,
        'nickname': 'Smart Lock',
        'createdAt': int(datetime.datetime.now().strftime("%s")) * 1000,
        'timezone': 'US/Eastern',
    }
    response_json = response.get_json()

    # We don't particularly care what id it is
    assert 'id' in response_json
    expected_json['id'] = response_json['id']

    assert response.status_code == 200
    assert response_json == expected_json


@freeze_time("August, 1, 2019")
def test_post_lock_with_args_admin(
    client,
    id_token,
    seeded_admin_user,
):
    response = client.post(
        '/api/v1/admin/locks',
        headers={
            'Authorization': id_token,
        },
        json={
            'nickname': 'FOOBAR',
            'timezone': 'Europe/London',
        }
    )
    expected_json = {
        'status': LockStatus.CLOSED.value,
        'nickname': 'FOOBAR',
        'createdAt': int(datetime.datetime.now().strftime("%s")) * 1000,
        'timezone': 'Europe/London',
    }
    response_json = response.get_json()

    # We don't particularly care what id it is
    assert 'id' in response_json
    expected_json['id'] = response_json['id']

    assert response.status_code == 200
    assert response_json == expected_json
