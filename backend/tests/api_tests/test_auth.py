AUTH_ROUTE_PREFIX = "/auth"
REGISTRATION_ROUTE = f"{AUTH_ROUTE_PREFIX}/register"
TOKEN_ROUTE = f"{AUTH_ROUTE_PREFIX}/token"


class TestRegistration:
    def test_register(self, client):
        response = client.post(
            REGISTRATION_ROUTE,
            json={"username": "testuser2", "password": "testpassword"},
        )
        assert response.status_code == 200

        user = response.json()
        assert user["username"] == "testuser2"
        assert "hashed_password" not in user

    def test_register_existing_user(self, client):
        client.post(
            REGISTRATION_ROUTE,
            json={"username": "testuser2", "password": "testpassword"},
        )

        response = client.post(
            REGISTRATION_ROUTE,
            json={"username": "testuser2", "password": "testpassword"},
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Username already registered."}


class TestLogin:
    def test_login(self, client):
        # Make sure the user is registered before attempting to log in
        client.post(
            REGISTRATION_ROUTE,
            json={"username": "testuser2", "password": "testpassword"},
        )

        response = client.post(
            TOKEN_ROUTE,
            data={"username": "testuser2", "password": "testpassword"},
        )
        assert response.status_code == 200

        token = response.json()
        assert "access_token" in token
        assert token["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client):
        client.post(
            REGISTRATION_ROUTE,
            json={"username": "testuser2", "password": "testpassword"},
        )

        response = client.post(
            TOKEN_ROUTE,
            data={"username": "testuser2", "password": "wrongpassword"},
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect username or password"}

    def test_login_nonexistent_user(self, client):
        response = client.post(
            TOKEN_ROUTE,
            data={"username": "nonexistentuser", "password": "testpassword"},
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect username or password"}
