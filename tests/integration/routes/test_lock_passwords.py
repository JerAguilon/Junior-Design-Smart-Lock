import pytest

from freezegun import freeze_time

from document_templates.password import PasswordDays


def test_get_passwords_unauthorized(client):
    response = client.get('/api/v1/locks/foobar/passwords')
    assert response.status_code == 401
    assert 'message' in response.get_json()


@pytest.mark.usefixtures("seeded_user_lock")
def test_get_passwords_authorized(
        client,
        id_token,
        seeded_user,
        seeded_password,
        seeded_lock):
    response = client.get(
        '/api/v1/locks/{}/passwords'.format(seeded_lock.id),
        headers={
            'Authorization': id_token,
        },
    )
    expected_json = {
        'otp': [],
        'permanent': [
            {
                'expiration': seeded_password.expiration,
                'id': seeded_password.id,
                'type': seeded_password.type.value,
                'createdAt': seeded_password.created_at,
                'activeDays': seeded_password.active_days,
                'activeTimes': seeded_password.active_times,
            }
        ]
    }
    assert response.status_code == 200
    assert response.get_json() == expected_json


@freeze_time("August, 1, 2019")
@pytest.mark.usefixtures("seeded_user_lock")
def test_post_password(
        client,
        id_token,
        seeded_user,
        mock_password,
        seeded_lock):
    mock_password.active_days = [
        PasswordDays.MONDAY, PasswordDays.TUESDAY
    ]
    response = client.post(
        '/api/v1/locks/{}/passwords'.format(seeded_lock.id),
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
    expected_json = {
        'type': mock_password.type.value,
        'expiration': mock_password.expiration,
        'createdAt': mock_password.created_at,
        'activeDays': [day.value for day in mock_password.active_days],
        'activeTimes': ['12:00', '24:00']
    }
    response_json = response.get_json()
    del response_json['id']
    assert response.status_code == 200
    assert response_json == expected_json
