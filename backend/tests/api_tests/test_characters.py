from sqlalchemy.ext.asyncio import AsyncSession

from tests.failures import async_failure, sync_failure

CHARACTERS_ROUTE = "/characters/"


class TestCharacterCreate:
    def test_create_character(self, shared_auth_client, character_payload):
        response = shared_auth_client.post(
            CHARACTERS_ROUTE, json=character_payload
        )
        assert response.status_code == 201
        returned_character = response.json()

        # Deal with actions separately since they are transformed in response
        actions_dict = character_payload.pop("actions")
        for attack in actions_dict["attacks"]:
            assert any(
                created_attack["name"].lower() == attack.lower()
                for created_attack in returned_character["actions"]["attacks"]
            )
        for spell in actions_dict["spells"].keys():
            assert any(
                created_spell["name"].lower().replace(" ", "_")
                == spell.lower()
                for created_spell in returned_character["actions"]["spells"]
            )
        assert returned_character["actions"]["shield"] == actions_dict.get(
            "shield", 0
        )
        assert returned_character["actions"]["heals"] == actions_dict.get(
            "heals"
        )
        assert returned_character["actions"][
            "sneak_attack"
        ] == actions_dict.get("sneak_attack", False)

        for key, value in character_payload.items():
            assert returned_character[key] == value

    def test_create_character_unauthenticated(self, client, character_payload):
        request = character_payload
        response = client.post(CHARACTERS_ROUTE, json=request)
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    def test_create_character_invalid(self, shared_auth_client):
        request = {"name": "Invalid"}
        response = shared_auth_client.post(CHARACTERS_ROUTE, json=request)
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Field required"

    def test_create_character_internal_error(
        self, shared_auth_client, character_payload, monkeypatch
    ):
        monkeypatch.setattr(
            "api.routes.characters.convert_to_db_character", sync_failure
        )
        request = character_payload
        response = shared_auth_client.post(CHARACTERS_ROUTE, json=request)
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"


class TestCharacterRead:
    def test_read_characters_list(self, auth_client, owned_character_factory):
        fighter = owned_character_factory()
        wizard = owned_character_factory("wizard")
        rogue = owned_character_factory("rogue")
        cleric = owned_character_factory("cleric")
        characters = {
            fighter["id"]: fighter,
            wizard["id"]: wizard,
            rogue["id"]: rogue,
            cleric["id"]: cleric,
        }
        response = auth_client.get(CHARACTERS_ROUTE)
        assert response.status_code == 200

        character_list = response.json()
        assert len(character_list) == 4
        for character in character_list:
            assert character["id"] in characters
            for key, value in characters[character["id"]].items():
                assert character[key] == value

    def test_read_character(self, auth_client, created_character):
        response = auth_client.get(
            f"{CHARACTERS_ROUTE}{created_character['id']}/"
        )
        assert response.status_code == 200
        returned_character = response.json()
        for key, value in created_character.items():
            assert returned_character[key] == value

    def test_read_characters_list_unauthenticated(self, client):
        response = client.get(CHARACTERS_ROUTE)
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    def test_read_characters_list_internal_error(
        self, shared_auth_client, monkeypatch
    ):
        monkeypatch.setattr(
            "api.routes.characters.fetch_characters_from_db", sync_failure
        )
        response = shared_auth_client.get(CHARACTERS_ROUTE)
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"

    def test_read_character_unauthenticated(self, client):
        response = client.get(f"{CHARACTERS_ROUTE}1/")
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    def test_read_character_not_found(self, shared_auth_client):
        response = shared_auth_client.get(f"{CHARACTERS_ROUTE}9999999/")
        assert response.status_code == 404
        assert response.json()["detail"] == "character not found"

    def test_read_character_forbidden(
        self, shared_auth_client, created_character
    ):
        response = shared_auth_client.get(
            f"{CHARACTERS_ROUTE}{created_character['id']}/"
        )
        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "Not authorized to view this character"
        )

    def test_read_character_internal_error(
        self, shared_auth_client, monkeypatch
    ):
        monkeypatch.setattr(AsyncSession, "get", async_failure)
        response = shared_auth_client.get(f"{CHARACTERS_ROUTE}1/")
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"


class TestCharacterUpdate:
    def test_update_character(self, auth_client, created_character):
        actions_dict = created_character.pop("actions")
        character_name = created_character.pop("name")
        # Add new attack
        actions_dict["attacks"] = [
            attack["name"] for attack in actions_dict["attacks"]
        ] + ["warhammer"]
        spells_dict = {
            spell["name"].lower().replace(" ", "_"): spell["slots"]
            for spell in actions_dict["spells"]
        }

        # Add new spell
        spells_dict["breathe_fire"] = 1
        actions_dict["spells"] = spells_dict

        request = {
            "name": f"{character_name}_updated",
            "actions": actions_dict,
        }
        character_id = created_character["id"]
        response = auth_client.patch(
            f"{CHARACTERS_ROUTE}{character_id}/", json=request
        )
        assert response.status_code == 200

        character_data = response.json()

        # Check that the name and actions were updated correctly
        assert character_data["name"] == f"{character_name}_updated"
        assert any(
            created_attack["name"].lower() == "warhammer"
            for created_attack in character_data["actions"]["attacks"]
        )
        assert any(
            created_spell["name"].lower().replace(" ", "_") == "breathe_fire"
            for created_spell in character_data["actions"]["spells"]
        )

        # Check that other fields remain unchanged
        for key, value in created_character.items():
            assert character_data[key] == value

        for attack in actions_dict["attacks"]:
            assert any(
                created_attack["name"].lower() == attack.lower()
                for created_attack in character_data["actions"]["attacks"]
            )
        for spell in actions_dict["spells"].keys():
            assert any(
                created_spell["name"].lower().replace(" ", "_")
                == spell.lower()
                for created_spell in character_data["actions"]["spells"]
            )
        assert character_data["actions"]["shield"] == actions_dict.get(
            "shield", 0
        )
        assert character_data["actions"]["heals"] == actions_dict.get("heals")
        assert character_data["actions"]["sneak_attack"] == actions_dict.get(
            "sneak_attack", False
        )

    def test_update_character_unauthenticated(self, client):
        request = {"name": "test"}
        response = client.patch(f"{CHARACTERS_ROUTE}1/", json=request)
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    def test_update_character_invalid(self, shared_auth_client):
        response = shared_auth_client.patch(f"{CHARACTERS_ROUTE}1/")
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Field required"

    def test_update_character_not_found(self, shared_auth_client):
        request = {"name": "test"}
        response = shared_auth_client.patch(
            f"{CHARACTERS_ROUTE}999999999/", json=request
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "character not found"

    def test_update_character_forbidden(
        self, shared_auth_client, created_character
    ):
        request = {"name": "test"}
        response = shared_auth_client.patch(
            f"{CHARACTERS_ROUTE}{created_character['id']}/", json=request
        )
        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "Not authorized to update this character"
        )

    def test_update_character_internal_error(
        self, shared_auth_client, monkeypatch
    ):
        monkeypatch.setattr(AsyncSession, "get", async_failure)
        request = {"name": "test"}
        response = shared_auth_client.patch(
            f"{CHARACTERS_ROUTE}1/", json=request
        )
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"


class TestCharacterDelete:
    def test_delete_character(self, auth_client, character_payload):
        creation_response = auth_client.post(
            CHARACTERS_ROUTE, json=character_payload
        )
        created_character = creation_response.json()
        character_id = created_character["id"]
        response = auth_client.delete(f"{CHARACTERS_ROUTE}{character_id}/")
        assert response.status_code == 200

        response = auth_client.get(f"{CHARACTERS_ROUTE}{character_id}/")
        assert response.status_code == 404

    def test_delete_character_unauthenticated(self, client):
        response = client.delete(f"{CHARACTERS_ROUTE}1/")
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    def test_delete_character_not_found(self, shared_auth_client):
        response = shared_auth_client.delete(f"{CHARACTERS_ROUTE}999999999/")
        assert response.status_code == 404
        assert response.json()["detail"] == "character not found"

    def test_delete_character_forbidden(
        self, shared_auth_client, created_character
    ):
        response = shared_auth_client.delete(
            f"{CHARACTERS_ROUTE}{created_character['id']}/"
        )
        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "Not authorized to delete this character"
        )

    def test_delete_character_internal_error(
        self, auth_client, created_character, monkeypatch
    ):
        monkeypatch.setattr(AsyncSession, "delete", async_failure)
        response = auth_client.delete(
            f"{CHARACTERS_ROUTE}{created_character['id']}/"
        )
        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"
