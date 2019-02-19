import base64

from freezegun import freeze_time

from document_templates.lock import LockStatus


TEST_PASSWORD = "testpassword1234"
FROZEN_TIME = "August, 1, 2019"


def create_lock(
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
            'secret': TEST_PASSWORD,
        }
    )
    assert response.status_code == 200
    return response.get_json()


@freeze_time(FROZEN_TIME)
def test_get_lock_status_unauthorized(
    client,
    id_token,
    seeded_admin_user,
):
    lock_id = create_lock(client, id_token, seeded_admin_user)['id']
    user_pass = base64.b64encode("{}:{}".format(
        lock_id, "INVALID").encode()).decode('ascii')

    response = client.get(
        '/api/v1/hardware/status',
        headers={
            'Authorization': 'Basic ' + user_pass,
        },
    )
    expected_json = {
        'error': 'Invalid secret supplied'
    }
    response_json = response.get_json()
    assert response.status_code == 401
    assert response_json == expected_json


@freeze_time(FROZEN_TIME)
def test_get_lock_status_authorized(
    client,
    id_token,
    seeded_admin_user,
):
    lock_id = create_lock(client, id_token, seeded_admin_user)['id']
    user_pass = base64.b64encode(
        "{}:{}".format(
            lock_id,
            TEST_PASSWORD).encode()).decode('ascii')

    response = client.get(
        '/api/v1/hardware/status',
        headers={
            'Authorization': 'Basic ' + user_pass,
        },
    )
    expected_json = {
        'status': LockStatus.CLOSED.value,
    }
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json == expected_json


@freeze_time(FROZEN_TIME)
def test_put_lock_status_authorized(
    client,
    id_token,
    seeded_admin_user,
):
    lock_id = create_lock(client, id_token, seeded_admin_user)['id']
    user_pass = base64.b64encode(
        "{}:{}".format(
            lock_id,
            TEST_PASSWORD).encode()).decode('ascii')

    response = client.put(
        '/api/v1/hardware/status',
        json={
            'status': LockStatus.OPEN.value,
        },
        headers={
            'Authorization': 'Basic ' + user_pass,
        },
    )
    expected_json = {
        'status': LockStatus.OPEN.value,
    }
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json == expected_json
