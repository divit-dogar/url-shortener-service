from .conftest import client
import uuid

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
            "custom_alias": f"pytest-{uuid.uuid4().hex[:6]}",
            "expires_at": None,
        },
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 201