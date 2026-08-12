from tests.failures import sync_failure


def test_read_user(shared_auth_client, shared_auth_username):
    response = shared_auth_client.get("/users/me/")
    assert response.status_code == 200
    assert response.json()["username"] == shared_auth_username


def test_read_user_unauthenticated(client):
    response = client.get("/users/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_read_user_invalid_token(client):
    response = client.get(
        "/users/me/", headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_update_user(auth_client, test_username):
    request = {
        "username": f"{test_username}_updated",
        "old_password": "testpassword",
        "password": "testpassword",
    }
    response = auth_client.patch("/users/", json=request)
    assert response.status_code == 200
    assert response.json()["username"] == f"{test_username}_updated"


def test_update_user_wrong_password(auth_client, test_username):
    request = {
        "username": f"{test_username}_updated",
        "old_password": "wrong",
    }
    response = auth_client.patch("/users/", json=request)
    assert response.status_code == 400


def test_update_user_existing_username(auth_client):
    request = {
        "username": "testuser",
        "old_password": "testpassword",
    }
    response = auth_client.patch("/users/", json=request)
    assert response.status_code == 400


def test_update_user_internal_error(auth_client, test_username, monkeypatch):
    monkeypatch.setattr("api.routes.users.verify_password", sync_failure)
    request = {
        "username": f"{test_username}_updated",
        "old_password": "testpassword",
        "password": "testpassword",
    }
    response = auth_client.patch("/users/", json=request)
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal Server Error"


def test_delete_user(auth_client):
    request = {"password": "testpassword"}
    response = auth_client.delete("/users/", json=request)
    assert response.status_code == 204
    assert response.content == b""


def test_delete_user_wrong(auth_client):
    request = {"password": "wrongpassword"}
    response = auth_client.delete("/users/", json=request)
    assert response.status_code == 400
    assert response.json()["detail"] == "Password invalid. Please try again"


def test_delete_user_internal_error(auth_client, monkeypatch):
    monkeypatch.setattr("api.routes.users.verify_password", sync_failure)
    request = {"password": "testpassword"}
    response = auth_client.delete("/users/", json=request)
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal Server Error"
