from .conftest import client


def test_get_analytics():

    login = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "Password@123",
        },
    )

    token = login.json()["access_token"]

    response = client.get(
        "/analytics/pytest",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code in [200, 404]