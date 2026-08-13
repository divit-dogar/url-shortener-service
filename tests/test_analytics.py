import uuid

from .conftest import client


def test_get_analytics():

    # Login
    login = client.post(
        "/auth/login",
        json={
            "username": "test@example.com",
            "password": "Password@123",
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Generate a unique alias for every test run
    custom_alias = f"analytics-{uuid.uuid4().hex[:8]}"

    # Create URL
    create_response = client.post(
        "/urls",
        headers=headers,
        json={
            "original_url": "https://google.com",
            "custom_alias": custom_alias,
            "expires_at": None,
        },
    )

    assert create_response.status_code == 201

    # Get the AUTO-GENERATED short code from response
    created_url = create_response.json()
    short_code = created_url["short_code"]
    
    # Visit short URL -> generates click event
    click_response = client.get(
        f"/{short_code}",
        follow_redirects=False,
    )

    assert click_response.status_code == 302

    # Get analytics
    response = client.get(
        f"/analytics/{short_code}",
        headers=headers,
    )

    print("ANALYTICS STATUS:", response.status_code)
    print("ANALYTICS RESPONSE:", response.json())

    assert response.status_code == 200
    
    data = response.json()

    assert data["short_code"] == short_code
    assert data["total_clicks"] >= 1