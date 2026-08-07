from .conftest import client


def test_register():

    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "Password@123",
        },
    )

    assert response.status_code in [201, 400]


def test_login():

    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data