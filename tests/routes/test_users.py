def test_get_user_unauthorized(client, id_token):
    response = client.get('/api/v1/user')
    assert response.status_code == 401
    assert 'message' in response.get_json()


def test_get_user(client, id_token):
    print(id_token)
    response = client.get(
        '/api/v1/user',
        headers={'Authorization': id_token}
    )
    expected_json = {
        'id': 'dk3vrI9xs4UX0mmWSsSSmHcslkH3',
        'email': 'test_user@test.com',
        'displayName': ''}
    assert response.status_code == 200
    assert response.get_json() == expected_json
