def test_read_character(auth_client, created_character):
    response = auth_client.get(f"/characters/{created_character['id']}/")
    assert response.status_code == 200
    character_data = response.json()
    for key in created_character.keys():
        assert character_data[key] == created_character[key]


def test_read_characters(auth_client, character_factory):
    fighter = character_factory()
    wizard = character_factory("wizard")
    rogue = character_factory("rogue")
    cleric = character_factory("cleric")
    characters = {
        fighter["id"]: fighter,
        wizard["id"]: wizard,
        rogue["id"]: rogue,
        cleric["id"]: cleric,
    }
    response = auth_client.get("/characters/")
    assert response.status_code == 200
    character_list = response.json()
    assert len(character_list) == 4
    for character in character_list:
        assert character["id"] in characters
        for key in characters[character["id"]].keys():
            assert character[key] == characters[character["id"]][key]


def test_create_character(auth_client, character_payload):
    request = character_payload
    response = auth_client.post("/characters/", json=request)
    assert response.status_code == 201
    character_data = response.json()

    # Deal with actions separately since they are transformed in response
    actions_dict = character_payload.pop("actions")
    for attack in actions_dict["attacks"]:
        assert any(
            created_attack["name"].lower() == attack.lower()
            for created_attack in character_data["actions"]["attacks"]
        )
    for spell in actions_dict["spells"].keys():
        assert any(
            created_spell["name"].lower().replace(" ", "_") == spell.lower()
            for created_spell in character_data["actions"]["spells"]
        )
    assert character_data["actions"]["shield"] == actions_dict.get("shield", 0)
    assert character_data["actions"]["heals"] == actions_dict.get("heals")
    assert character_data["actions"]["sneak_attack"] == actions_dict.get(
        "sneak_attack", False
    )

    for key in character_payload.keys():
        assert character_data[key] == character_payload[key]


def test_update_character(auth_client, created_character):
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
    response = auth_client.patch(f"/characters/{character_id}", json=request)
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
    for key in created_character.keys():
        assert character_data[key] == created_character[key]

    for attack in actions_dict["attacks"]:
        assert any(
            created_attack["name"].lower() == attack.lower()
            for created_attack in character_data["actions"]["attacks"]
        )
    for spell in actions_dict["spells"].keys():
        assert any(
            created_spell["name"].lower().replace(" ", "_") == spell.lower()
            for created_spell in character_data["actions"]["spells"]
        )
    assert character_data["actions"]["shield"] == actions_dict.get("shield", 0)
    assert character_data["actions"]["heals"] == actions_dict.get("heals")
    assert character_data["actions"]["sneak_attack"] == actions_dict.get(
        "sneak_attack", False
    )


def test_delete_character(auth_client, created_character):
    character_id = created_character["id"]
    response = auth_client.delete(f"/characters/{character_id}")
    assert response.status_code == 200

    response = auth_client.get(f"/characters/{character_id}")
    assert response.status_code == 404
