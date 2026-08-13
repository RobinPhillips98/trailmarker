import json

from tests.failures import sync_failure
from tests.sample_imports import (
    import_cleric_data,
    import_fighter_data,
    import_rogue_data,
    import_wizard_data,
)

IMPORT_ROUTE = "/characters/import"


def test_import_character_fighter(shared_auth_client, import_payload_fighter):
    response = shared_auth_client.post(
        IMPORT_ROUTE, json=import_payload_fighter
    )
    assert response.status_code == 201
    created_character = response.json()
    import_fighter_data.pop("user_id")
    for key, value in import_fighter_data.items():
        assert created_character[key] == value


def test_import_character_cleric(shared_auth_client, import_payload_cleric):
    response = shared_auth_client.post(
        IMPORT_ROUTE, json=import_payload_cleric
    )
    assert response.status_code == 201
    created_character = response.json()
    for spell in created_character["actions"]["spells"]:
        spell.pop("description")
    import_cleric_data.pop("user_id")
    for key, value in import_cleric_data.items():
        assert created_character[key] == value


def test_import_character_rogue(shared_auth_client, import_payload_rogue):
    response = shared_auth_client.post(IMPORT_ROUTE, json=import_payload_rogue)
    assert response.status_code == 201
    created_character = response.json()
    import_rogue_data.pop("user_id")
    for key, value in import_rogue_data.items():
        assert created_character[key] == value


def test_import_character_wizard(shared_auth_client, import_payload_wizard):
    response = shared_auth_client.post(
        IMPORT_ROUTE, json=import_payload_wizard
    )
    assert response.status_code == 201
    created_character = response.json()
    created_character["actions"]["spells"].pop()
    import_wizard_data["actions"]["spells"].pop()
    for spell in created_character["actions"]["spells"]:
        spell.pop("description")

    import_wizard_data.pop("user_id")
    print(json.dumps(created_character, indent=4))
    for key, value in import_wizard_data.items():
        assert created_character[key] == value


def test_import_character_unauthenticated(client, import_payload_fighter):
    response = client.post(IMPORT_ROUTE, json=import_payload_fighter)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_import_character_invalid(shared_auth_client):
    request = {"name": "invalid"}
    response = shared_auth_client.post(IMPORT_ROUTE, json=request)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"


def test_import_character_internal_error(
    shared_auth_client, import_payload_fighter, monkeypatch
):
    monkeypatch.setattr(
        "api.routes.characters.convert_to_db_character", sync_failure
    )
    response = shared_auth_client.post(
        IMPORT_ROUTE, json=import_payload_fighter
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal Server Error"
