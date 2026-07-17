def test_register(client):
    response = client.post(
        "/auth/register",
        json={"username": "testuser2", "password": "testpassword"},
    )
    assert response.status_code == 200

    user = response.json()
    assert user["username"] == "testuser2"
    assert "hashed_password" not in user


def test_register_existing_user(client):
    response = client.post(
        "/auth/register",
        json={"username": "testuser2", "password": "testpassword"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered."}


def test_login(client):
    response = client.post(
        "/auth/token",
        data={"username": "testuser2", "password": "testpassword"},
    )
    assert response.status_code == 200

    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/token",
        data={"username": "testuser2", "password": "wrongpassword"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect username or password"}
