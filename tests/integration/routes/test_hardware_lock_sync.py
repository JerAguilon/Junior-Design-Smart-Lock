import base64

from freezegun import freeze_time


TEST_PASSWORD = "testpassword1234"


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


def create_password(
    client,
    id_token,
    lock_id,
    seeded_user,
    mock_password,
    db
):
    db.child("UserLocks").child(seeded_user.id).set(
        {
            "ownedLockIds": [lock_id]
        }
    )
    client.post(
        '/api/v1/locks/{}/passwords'.format(lock_id),
        headers={
            'Authorization': id_token,
        },
        json={
            'password': '123456',
            'type': mock_password.type.value,
            'activeDays': [day.value for day in mock_password.active_days],
            'activeTimes': ['12:00', '24:00']
        }
    )


def test_sync_unauthorized(
    client,
    id_token,
    seeded_admin_user,
):
    lock_id = create_lock(client, id_token, seeded_admin_user)['id']
    user_pass = base64.b64encode("{}:{}".format(
        lock_id, "INVALID").encode()).decode('ascii')

    response = client.get(
        '/api/v1/hardware/sync',
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


@freeze_time("August 1, 2019")
def test_sync_authorized(
    client,
    db,
    id_token,
    mock_password,
    seeded_admin_user
):
    lock_id = create_lock(client, id_token, seeded_admin_user)['id']
    create_password(
        client,
        id_token,
        lock_id,
        seeded_admin_user,
        mock_password,
        db
    )

    user_pass = base64.b64encode(
        "{}:{}".format(
            lock_id,
            TEST_PASSWORD).encode()).decode('ascii')

    response = client.get(
        '/api/v1/hardware/sync',
        headers={
            'Authorization': 'Basic ' + user_pass,
        },
    )

    response_json = response.get_json()
    assert response.status_code == 200
    assert len(response_json['permanent']) == 1
    assert response_json['permanent'][0]
    assert response_json['permanent'][0]['hashedPassword']
