from .conftest import client


def test_dashboard():

    login = client.post(
        "/auth/login",
        json={
            "username": "test@example.com",
            "password": "Password@123",
        },
    )

    token = login.json()["access_token"]

    response = client.get(
        "/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200