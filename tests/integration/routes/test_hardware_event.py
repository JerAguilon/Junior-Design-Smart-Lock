import base64

from freezegun import freeze_time


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

    response = client.post(
        '/api/v1/hardware/events',
        json={
            'event': "HARDWARE_LOCK_OPENED"
        },
        headers={
            'Authorization': 'Basic ' + user_pass,
        },
    )
    assert response.status_code == 200, response.get_json()
