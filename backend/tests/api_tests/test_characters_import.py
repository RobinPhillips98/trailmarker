import json

from tests.sample_imports import (
    import_cleric_data,
    import_fighter_data,
    import_rogue_data,
    import_wizard_data,
)


def test_import_character_fighter(shared_auth_client, import_payload_fighter):
    response = shared_auth_client.post(
        "/characters/import", json=import_payload_fighter
    )
    assert response.status_code == 201
    created_character = response.json()
    import_fighter_data.pop("user_id")
    for key in import_fighter_data.keys():
        assert created_character[key] == import_fighter_data[key]


def test_import_character_cleric(shared_auth_client, import_payload_cleric):
    response = shared_auth_client.post(
        "/characters/import", json=import_payload_cleric
    )
    assert response.status_code == 201
    created_character = response.json()
    for spell in created_character["actions"]["spells"]:
        spell.pop("description")
    import_cleric_data.pop("user_id")
    for key in import_cleric_data.keys():
        assert created_character[key] == import_cleric_data[key]


def test_import_character_rogue(shared_auth_client, import_payload_rogue):
    response = shared_auth_client.post(
        "/characters/import", json=import_payload_rogue
    )
    assert response.status_code == 201
    created_character = response.json()
    import_rogue_data.pop("user_id")
    for key in import_rogue_data.keys():
        assert created_character[key] == import_rogue_data[key]


def test_import_character_wizard(shared_auth_client, import_payload_wizard):
    response = shared_auth_client.post(
        "/characters/import", json=import_payload_wizard
    )
    assert response.status_code == 201
    created_character = response.json()
    created_character["actions"]["spells"].pop()
    import_wizard_data["actions"]["spells"].pop()
    for spell in created_character["actions"]["spells"]:
        spell.pop("description")

    import_wizard_data.pop("user_id")
    print(json.dumps(created_character, indent=4))
    for key in import_wizard_data.keys():
        assert created_character[key] == import_wizard_data[key]
