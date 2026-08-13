from sqlalchemy.ext.asyncio import AsyncSession

from tests.failures import async_failure, sync_failure

ENCOUNTERS_ROUTE = "/encounters/"


class TestEncounterCreate:
    def test_create_encounter(self, shared_auth_client, encounter_payload):
        response = shared_auth_client.post(
            ENCOUNTERS_ROUTE, json=encounter_payload
        )
        assert response.status_code == 201

        returned_encounter = response.json()

        assert "id" in returned_encounter.keys()
        assert returned_encounter["name"] == encounter_payload["name"]
        assert returned_encounter["enemies"] == encounter_payload["enemies"]

    def test_create_encounter_unauthenticated(self, client, encounter_payload):
        response = client.post(ENCOUNTERS_ROUTE, json=encounter_payload)
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    def test_create_encounter_invalid(self, shared_auth_client):
        request = {"name": "Invalid"}
        response = shared_auth_client.post(ENCOUNTERS_ROUTE, json=request)
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Field required"

    def test_create_encounter_internal_error(
        self, shared_auth_client, encounter_payload, monkeypatch
    ):
        monkeypatch.setattr(AsyncSession, "add", sync_failure)
        response = shared_auth_client.post(
            ENCOUNTERS_ROUTE, json=encounter_payload
        )
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"


class TestEncounterRead:
    def test_read_encounters_list(self, auth_client, encounter_factory):
        for i in range(4):
            encounter_factory()
        response = auth_client.get(ENCOUNTERS_ROUTE)
        assert response.status_code == 200
        encounter_list = response.json()
        assert len(encounter_list) == 4
        for encounter in encounter_list:
            assert "id" in encounter.keys()
            assert "name" in encounter.keys()
            assert encounter["enemies"] == [{"id": 1, "quantity": 2}]

    def test_read_encounter(self, auth_client, created_encounter):
        encounter_id = created_encounter["id"]
        response = auth_client.get(f"{ENCOUNTERS_ROUTE}{encounter_id}")
        assert response.status_code == 200
        returned_encounter = response.json()

        assert returned_encounter["id"] == encounter_id
        assert returned_encounter["name"] == created_encounter["name"]
        assert returned_encounter["enemies"] == created_encounter["enemies"]

    def test_read_encounters_unauthenticated(self, client):
        response = client.get(ENCOUNTERS_ROUTE)
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    def test_read_encounters_internal_error(
        self, shared_auth_client, monkeypatch
    ):
        monkeypatch.setattr(AsyncSession, "scalars", async_failure)
        response = shared_auth_client.get(ENCOUNTERS_ROUTE)
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"

    def test_read_encounter_unauthenticated(self, client):
        response = client.get(f"{ENCOUNTERS_ROUTE}1")
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    def test_read_encounter_not_found(self, shared_auth_client):
        response = shared_auth_client.get(f"{ENCOUNTERS_ROUTE}999999999")
        assert response.status_code == 404
        assert response.json()["detail"] == "encounter not found"

    def test_read_encounter_forbidden(
        self, shared_auth_client, created_encounter
    ):
        response = shared_auth_client.get(
            f"{ENCOUNTERS_ROUTE}{created_encounter["id"]}"
        )
        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "Not authorized to view this encounter"
        )

    def test_read_encounter_internal_error(
        self, shared_auth_client, monkeypatch
    ):
        monkeypatch.setattr(AsyncSession, "get", async_failure)
        response = shared_auth_client.get(f"{ENCOUNTERS_ROUTE}1")
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"


class TestEncounterUpdate:
    def test_update_encounter(self, auth_client, created_encounter):
        encounter_id = created_encounter["id"]
        request = {
            "name": f"{created_encounter["name"]}_updated",
            "enemies": [{"id": 1, "quantity": 2}, {"id": 2, "quantity": 1}],
        }
        response = auth_client.patch(
            f"{ENCOUNTERS_ROUTE}{encounter_id}", json=request
        )
        assert response.status_code == 200
        returned_encounter = response.json()

        assert returned_encounter["id"] == created_encounter["id"]
        assert (
            returned_encounter["name"]
            == f"{created_encounter["name"]}_updated"
        )
        assert returned_encounter["enemies"] == [
            {"id": 1, "quantity": 2},
            {"id": 2, "quantity": 1},
        ]

    def test_update_encounter_unauthenticated(self, client):
        request = {"name": "test"}
        response = client.patch(f"{ENCOUNTERS_ROUTE}1", json=request)
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    def test_update_encounter_invalid(self, shared_auth_client):
        response = shared_auth_client.patch(f"{ENCOUNTERS_ROUTE}1")
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Field required"

    def test_update_encounter_not_found(self, shared_auth_client):
        request = {"name": "test"}
        response = shared_auth_client.patch(
            f"{ENCOUNTERS_ROUTE}999999999", json=request
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "encounter not found"

    def test_update_encounter_forbidden(
        self, shared_auth_client, created_encounter
    ):
        request = {"name": "test"}
        response = shared_auth_client.patch(
            f"{ENCOUNTERS_ROUTE}{created_encounter["id"]}", json=request
        )
        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "Not authorized to update this encounter"
        )

    def test_update_encounter_internal_error(
        self, shared_auth_client, monkeypatch
    ):
        monkeypatch.setattr(AsyncSession, "get", async_failure)
        request = {"name": "test"}
        response = shared_auth_client.patch(
            f"{ENCOUNTERS_ROUTE}1", json=request
        )
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"


class TestEncounterDelete:
    def test_delete_encounter(self, shared_auth_client, encounter_payload):
        creation_response = shared_auth_client.post(
            ENCOUNTERS_ROUTE, json=encounter_payload
        )
        created_encounter = creation_response.json()
        encounter_id = created_encounter["id"]
        response = shared_auth_client.delete(
            f"{ENCOUNTERS_ROUTE}{encounter_id}"
        )
        assert response.status_code == 200

        response = shared_auth_client.get(f"{ENCOUNTERS_ROUTE}{encounter_id}")
        assert response.status_code == 404

    def test_delete_encounter_unauthenticated(self, client):
        response = client.delete(f"{ENCOUNTERS_ROUTE}1")
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    def test_delete_encounter_not_found(self, shared_auth_client):
        response = shared_auth_client.delete(f"{ENCOUNTERS_ROUTE}999999999")
        assert response.status_code == 404
        assert response.json()["detail"] == "encounter not found"

    def test_delete_encounter_forbidden(
        self, shared_auth_client, created_encounter
    ):
        response = shared_auth_client.delete(
            f"{ENCOUNTERS_ROUTE}{created_encounter['id']}"
        )
        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "Not authorized to delete this encounter"
        )

    def test_delete_encounter_internal_error(
        self, auth_client, created_encounter, monkeypatch
    ):
        monkeypatch.setattr(AsyncSession, "delete", async_failure)
        response = auth_client.delete(
            f"{ENCOUNTERS_ROUTE}{created_encounter['id']}"
        )
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"
