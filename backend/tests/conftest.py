import asyncio
import json
import os
import uuid
from pathlib import Path

# Set test DB env before importing app/db modules that create engines.
os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = "postgres://postgres:postgres@localhost:5432/TEST"
os.environ["SECRET_KEY"] = "secret-key-for-testing"

import pytest  # noqa: E402
from sqlalchemy import create_engine, text  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy.orm.session import close_all_sessions  # noqa: E402
from sqlalchemy_utils import drop_database  # noqa: E402

from db import get_db  # noqa: E402
from server import app  # noqa: E402
from tests.utils import (  # noqa: E402
    TEST_DATABASE_URL,
    dispose_test_engines,
    initialize_test_database,
    override_get_db,
)

TEST_PASSWORD = "testpassword"


def terminate_test_db_connections(db_url: str, db_name: str):
    admin_url = db_url.rsplit("/", 1)[0] + "/postgres"
    engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        conn.execute(
            text(
                """
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = :db_name
                  AND pid <> pg_backend_pid()
                """
            ),
            {"db_name": db_name},
        )
    engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def create_and_delete_database():
    initialize_test_database()
    yield
    close_all_sessions()
    asyncio.run(dispose_test_engines())
    terminate_test_db_connections(
        TEST_DATABASE_URL, TEST_DATABASE_URL.rsplit("/", 1)[-1]
    )
    drop_database(TEST_DATABASE_URL)


@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _register_and_login(client, username: str, password: str) -> str:
    register_response = client.post(
        "/auth/register",
        json={"username": username, "password": password},
    )
    assert register_response.status_code == 200

    token_response = client.post(
        "/auth/token",
        data={"username": username, "password": password},
    )
    assert token_response.status_code == 200
    return token_response.json()["access_token"]


@pytest.fixture(scope="session")
def shared_auth_username():
    return "shared_test_user"


@pytest.fixture(scope="session")
def shared_auth_token(client, shared_auth_username):
    return _register_and_login(client, shared_auth_username, TEST_PASSWORD)


@pytest.fixture(scope="session")
def shared_auth_headers(shared_auth_token):
    return {"Authorization": f"Bearer {shared_auth_token}"}


@pytest.fixture
def unique_test_username():
    return f"testuser_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def test_user_credentials(unique_test_username):
    return {"username": unique_test_username, "password": TEST_PASSWORD}


@pytest.fixture
def test_username(unique_test_username):
    return unique_test_username


def _build_auth_client(client, default_headers):
    class AuthClient:
        def request(self, method: str, url: str, **kwargs):
            headers = kwargs.pop("headers", {})
            return client.request(
                method,
                url,
                headers={**default_headers, **headers},
                **kwargs,
            )

        def get(self, url: str, **kwargs):
            return self.request("GET", url, **kwargs)

        def post(self, url: str, **kwargs):
            return self.request("POST", url, **kwargs)

        def patch(self, url: str, **kwargs):
            return self.request("PATCH", url, **kwargs)

        def delete(self, url: str, **kwargs):
            return self.request("DELETE", url, **kwargs)

    return AuthClient()


@pytest.fixture
def shared_auth_client(client, shared_auth_headers):
    return _build_auth_client(client, shared_auth_headers)


@pytest.fixture
def auth_token(client, test_user_credentials):
    return _register_and_login(
        client,
        test_user_credentials["username"],
        test_user_credentials["password"],
    )


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def auth_client(client, auth_headers):
    return _build_auth_client(client, auth_headers)


@pytest.fixture
def character_payload():
    payload = _load_character_template("fighter")
    payload["name"] = f"fighter_{uuid.uuid4().hex[:8]}"
    return payload


@pytest.fixture
def character_factory(auth_client):
    def create(template: str = "fighter", **overrides):
        payload = _load_character_template(template)
        payload["name"] = overrides.pop(
            "name", f"{template}_{uuid.uuid4().hex[:8]}"
        )

        for key, value in overrides.items():
            payload[key] = value

        response = auth_client.post("/characters/", json=payload)
        assert response.status_code == 201
        return response.json()

    return create


@pytest.fixture
def created_character(character_factory):
    return character_factory()


@pytest.fixture
def import_payload_fighter():
    return _load_import_payload("fighter")


@pytest.fixture()
def import_payload_cleric():
    return _load_import_payload("cleric")


@pytest.fixture()
def import_payload_wizard():
    return _load_import_payload("wizard")


@pytest.fixture()
def import_payload_rogue():
    return _load_import_payload("rogue")


def _load_import_payload(name: str) -> dict:
    path = Path("tests/data/imports") / f"{name}.json"
    payload = json.loads(path.read_text())["build"]
    return payload


def _load_character_template(name: str) -> dict:
    path = Path("data/characters") / f"{name}.json"
    payload = json.loads(path.read_text())
    payload.pop("id", None)
    payload.pop("user_id", None)
    return payload
