import base64


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
    result = client.post(
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
    assert result.status_code == 200
    return result.get_json()['id']


def test_delete_password(
    client,
    db,
    id_token,
    mock_password,
    seeded_admin_user
):
    lock_id = create_lock(client, id_token, seeded_admin_user)['id']
    pw_id_1 = create_password(
        client,
        id_token,
        lock_id,
        seeded_admin_user,
        mock_password,
        db
    )
    pw_id_2 = create_password(
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

    response = client.delete(
        '/api/v1/hardware/passwords',
        headers={
            'Authorization': 'Basic ' + user_pass,
        },
        json={
            'passwordIds': [pw_id_1]
        }
    )

    passwords = db.child('Locks').child(lock_id).child('passwords').get().val()
    assert response.status_code == 200, response.get_json()
    assert pw_id_1 not in passwords
    assert pw_id_2 in passwords
