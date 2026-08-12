from sqlalchemy.ext.asyncio import AsyncSession

from tests.failures import async_failure, sync_failure
from tests.sample_data import test_enemy_sneak


def test_enemies_get(client):
    response = client.get("/enemies")
    assert response.status_code == 200
    enemies = response.json()
    assert len(enemies) == 3
    assert enemies[0]["name"] == "Goblin Commando"
    assert enemies[1]["name"] == "Goblin Igniter"
    assert enemies[2]["name"] == "Goblin Warrior"


def test_enemies_get_internal_error(client, monkeypatch):
    monkeypatch.setattr(AsyncSession, "scalars", async_failure)
    response = client.get("/enemies")
    assert response.status_code == 500
    assert response.json()["detail"] == ("Internal Server Error")


def test_enemies_get_by_id(client):
    response = client.get("/enemies/1")
    assert response.status_code == 200
    enemy = response.json()
    assert enemy["id"] == 1
    assert enemy["name"] == "Goblin Warrior"
    assert enemy["level"] == -1
    assert enemy["perception"] == 2
    assert enemy["skills"] == {
        "acrobatics": 5,
        "arcana": None,
        "athletics": 2,
        "crafting": None,
        "deception": None,
        "diplomacy": None,
        "intimidation": None,
        "lore": None,
        "medicine": None,
        "nature": 1,
        "occultism": None,
        "performance": None,
        "religion": None,
        "society": None,
        "stealth": 5,
        "survival": None,
        "thievery": None,
    }
    assert enemy["attribute_modifiers"] == {
        "strength": 0,
        "constitution": 1,
        "dexterity": 3,
        "intelligence": 0,
        "wisdom": -1,
        "charisma": 1,
    }
    assert enemy["defenses"] == {
        "armor_class": 16,
        "saves": {"fortitude": 5, "reflex": 7, "will": 3},
    }
    assert enemy["max_hit_points"] == 6
    assert not enemy["spell_attack_bonus"]
    assert not enemy["spell_dc"]
    assert enemy["speed"] == 25
    assert enemy["actions"] == {
        "attacks": [
            {
                "name": "Shortsword",
                "attackBonus": 7,
                "damage": "1d6",
                "damageType": "slashing",
                "range": None,
                "traits": ["agile", "finesse", "versatile-p"],
            },
            {
                "name": "Shortbow",
                "attackBonus": 7,
                "damage": "1d6",
                "damageType": "piercing",
                "range": 60,
                "traits": ["deadly-d10", "reload-0"],
            },
        ],
        "spells": [],
        "heals": 0,
        "shield": 0,
        "sneak_attack": False,
    }
    assert enemy["traits"] == ["small", "goblin", "humanoid"]
    assert not enemy["immunities"]
    assert not enemy["weaknesses"]
    assert not enemy["resistances"]


def test_enemy_get_by_id_internal_error(client, monkeypatch):
    monkeypatch.setattr(AsyncSession, "get", async_failure)
    response = client.get("/enemies/1")
    assert response.status_code == 500
    assert response.json()["detail"] == ("Internal Server Error")


def test_enemies_get_by_invalid_id(client):
    response = client.get("/enemies/999")
    assert response.status_code == 404
    error = response.json()
    assert error["detail"] == "Enemy not found"


def test_enemies_post(client):
    request = {
        "name": test_enemy_sneak["name"],
        "level": test_enemy_sneak["level"],
        "perception": test_enemy_sneak["perception"],
        "skills": test_enemy_sneak["skills"],
        "attribute_modifiers": test_enemy_sneak["attribute_modifiers"],
        "defenses": test_enemy_sneak["defenses"],
        "max_hit_points": test_enemy_sneak["max_hit_points"],
        "spell_attack_bonus": test_enemy_sneak["spell_attack_bonus"],
        "spell_dc": test_enemy_sneak["spell_dc"],
        "speed": test_enemy_sneak["speed"],
        "actions": {
            "attacks": [
                attack["name"].replace(" ", "_").lower()
                for attack in test_enemy_sneak["actions"]["attacks"]
            ],
            "spells": {},
            "heals": test_enemy_sneak["actions"]["heals"],
            "shield": test_enemy_sneak["actions"]["shield"],
            "sneak_attack": test_enemy_sneak["actions"]["sneak_attack"],
        },
        "proficiencies": {"martial": 4, "simple": 4, "fists": 4},
        "extra_proficiencies": {},
        "traits": test_enemy_sneak["traits"],
        "immunities": test_enemy_sneak["immunities"],
        "weaknesses": test_enemy_sneak["weaknesses"],
        "resistances": test_enemy_sneak["resistances"],
        "use_finesse": True,
    }
    response = client.post(
        "/enemies/",
        json=request,
    )
    assert response.status_code == 201

    enemy = response.json()
    assert "id" in enemy

    assert enemy["name"] == test_enemy_sneak["name"]
    assert enemy["level"] == test_enemy_sneak["level"]
    assert enemy["perception"] == test_enemy_sneak["perception"]
    assert enemy["skills"] == test_enemy_sneak["skills"]
    assert (
        enemy["attribute_modifiers"] == test_enemy_sneak["attribute_modifiers"]
    )
    assert enemy["defenses"] == test_enemy_sneak["defenses"]
    assert enemy["max_hit_points"] == test_enemy_sneak["max_hit_points"]
    assert (
        enemy["spell_attack_bonus"] == test_enemy_sneak["spell_attack_bonus"]
    )
    assert enemy["spell_dc"] == test_enemy_sneak["spell_dc"]
    assert enemy["speed"] == test_enemy_sneak["speed"]
    assert enemy["actions"] == test_enemy_sneak["actions"]
    assert enemy["traits"] == test_enemy_sneak["traits"]
    assert enemy["immunities"] == test_enemy_sneak["immunities"]
    assert enemy["weaknesses"] == test_enemy_sneak["weaknesses"]
    assert enemy["resistances"] == test_enemy_sneak["resistances"]


def test_enemies_post_invalid(client):
    request = {"name": "Invalid"}
    response = client.post(
        "/enemies/",
        json=request,
    )
    assert response.status_code == 422


def test_enemy_post_internal_error(client, monkeypatch):
    monkeypatch.setattr("api.routes.enemies.convert_to_db_enemy", sync_failure)

    request = {
        "name": test_enemy_sneak["name"],
        "level": test_enemy_sneak["level"],
        "perception": test_enemy_sneak["perception"],
        "skills": test_enemy_sneak["skills"],
        "attribute_modifiers": test_enemy_sneak["attribute_modifiers"],
        "defenses": test_enemy_sneak["defenses"],
        "max_hit_points": test_enemy_sneak["max_hit_points"],
        "spell_attack_bonus": test_enemy_sneak["spell_attack_bonus"],
        "spell_dc": test_enemy_sneak["spell_dc"],
        "speed": test_enemy_sneak["speed"],
        "actions": {
            "attacks": [
                attack["name"].replace(" ", "_").lower()
                for attack in test_enemy_sneak["actions"]["attacks"]
            ],
            "spells": {},
            "heals": test_enemy_sneak["actions"]["heals"],
            "shield": test_enemy_sneak["actions"]["shield"],
            "sneak_attack": test_enemy_sneak["actions"]["sneak_attack"],
        },
        "proficiencies": {"martial": 4, "simple": 4, "fists": 4},
        "extra_proficiencies": {},
        "traits": test_enemy_sneak["traits"],
        "immunities": test_enemy_sneak["immunities"],
        "weaknesses": test_enemy_sneak["weaknesses"],
        "resistances": test_enemy_sneak["resistances"],
        "use_finesse": True,
    }

    response = client.post("/enemies/", json=request)
    assert response.status_code == 500
    assert response.json()["detail"] == ("Internal Server Error")


def test_enemies_patch(client):
    request = {
        "name": "Updated Goblin Warrior",
        "level": 0,
        "perception": 3,
        "skills": {
            "acrobatics": 6,
            "arcana": None,
            "athletics": 3,
            "crafting": None,
            "deception": None,
            "diplomacy": None,
            "intimidation": None,
            "lore": None,
            "medicine": None,
            "nature": 2,
            "occultism": None,
            "performance": None,
            "religion": None,
            "society": None,
            "stealth": 6,
            "survival": None,
            "thievery": None,
        },
        "attribute_modifiers": {
            "strength": 1,
            "constitution": 2,
            "dexterity": 4,
            "intelligence": 1,
            "wisdom": 0,
            "charisma": 2,
        },
        "defenses": {
            "armor_class": 17,
            "saves": {"fortitude": 6, "reflex": 8, "will": 4},
        },
        "max_hit_points": 8,
        "spell_attack_bonus": None,
        "spell_dc": None,
        "speed": 30,
        "actions": {
            "attacks": ["Longsword", "Shortbow"],
            "spells": {"breathe_fire": 1},
        },
        "proficiencies": {"martial": 4, "simple": 4, "fists": 4},
        "traits": ["medium", "goblin", "humanoid"],
        "immunities": ["sleep"],
        "weaknesses": {"fire": 2},
        "resistances": {"cold": 2},
    }
    response = client.patch(
        "/enemies/1",
        json=request,
    )
    assert response.status_code == 200

    enemy = response.json()
    assert enemy["id"] == 1
    assert enemy["name"] == request["name"]
    assert enemy["level"] == request["level"]
    assert enemy["perception"] == request["perception"]
    assert enemy["skills"] == request["skills"]
    assert enemy["attribute_modifiers"] == request["attribute_modifiers"]
    assert enemy["defenses"] == request["defenses"]
    assert enemy["max_hit_points"] == request["max_hit_points"]
    assert enemy["spell_attack_bonus"] == request["spell_attack_bonus"]
    assert enemy["spell_dc"] == request["spell_dc"]
    assert enemy["speed"] == request["speed"]

    assert enemy["actions"]["attacks"][0]["name"] == "Longsword"
    assert enemy["actions"]["attacks"][0]["attackBonus"] == 6
    assert enemy["actions"]["attacks"][0]["damage"] == "1d8+1"
    assert enemy["actions"]["attacks"][0]["damageType"] == "slashing"
    assert enemy["actions"]["attacks"][0]["range"] is None
    assert enemy["actions"]["attacks"][0]["traits"] == ["versatile-p"]

    assert enemy["actions"]["attacks"][1]["name"] == "Shortbow"
    assert enemy["actions"]["attacks"][1]["attackBonus"] == 9
    assert enemy["actions"]["attacks"][1]["damage"] == "1d6"
    assert enemy["actions"]["attacks"][1]["damageType"] == "piercing"
    assert enemy["actions"]["attacks"][1]["range"] == 60
    assert enemy["actions"]["attacks"][1]["traits"] == ["deadly-d10"]

    spell = enemy["actions"]["spells"][0]
    assert spell["name"] == "Breathe Fire"
    assert spell["level"] == 1
    assert spell["damage_roll"] == "2d6"
    assert spell["damage_type"] == "fire"
    assert spell["range"] == 5
    assert spell["area"]["type"] == "cone"
    assert spell["area"]["value"] == "15"
    assert spell["save"] == "reflex"
    assert spell["targets"] == 0
    assert spell["actions"] == "2"
    assert (
        spell["description"]
        == "A gout of flame sprays from your mouth in a 15-foot cone. The fire deals 2d6 fire damage to each creature in the area. Each creature must roll a basic Reflex save."  # noqa: E501
    )

    assert enemy["traits"] == request["traits"]
    assert enemy["immunities"] == request["immunities"]
    assert enemy["weaknesses"] == request["weaknesses"]
    assert enemy["resistances"] == request["resistances"]


def test_enemies_patch_invalid(client):
    request = {"name": "Updated Goblin Warrior"}
    response = client.patch(
        "/enemies/999",
        json=request,
    )
    assert response.status_code == 404
    error = response.json()
    assert error["detail"] == "Enemy not found"


def test_enemy_patch_internal_error(client, monkeypatch):
    monkeypatch.setattr("api.routes.enemies.build_attack_list", sync_failure)

    request = {"actions": {"attacks": ["Longsword"], "spells": {}}}
    response = client.patch("/enemies/1", json=request)
    assert response.status_code == 500
    assert response.json()["detail"] == ("Internal Server Error")


def test_enemy_delete_internal_error(client, monkeypatch):
    monkeypatch.setattr(AsyncSession, "delete", async_failure)
    response = client.delete("/enemies/1")
    assert response.status_code == 500
    assert response.json()["detail"] == ("Internal Server Error")


def test_enemies_delete(client):
    response = client.delete("/enemies/1")
    assert response.status_code == 200

    assert response.json() == {"message": "Enemy deleted successfully."}

    # Verify that the enemy was deleted
    response = client.get("/enemies/1")
    assert response.status_code == 404


def test_enemies_delete_invalid(client):
    response = client.delete("/enemies/999")
    assert response.status_code == 404
    error = response.json()
    assert error["detail"] == "Enemy not found"
