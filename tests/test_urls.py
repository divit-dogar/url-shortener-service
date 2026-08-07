from .conftest import client


def test_create_url():

    login = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "Password@123",
        },
    )

    token = login.json()["access_token"]

    response = client.post(
        "/urls",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "original_url": "https://google.com",
            "custom_alias": "pytest",
            "expires_at": None,
        },
    )

    assert response.status_code == 201