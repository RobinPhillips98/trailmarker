from fastapi import APIRouter, Depends, status

import models
from schemas import Character, Enemy, SimData, SimRequest

from ..auth_helpers import get_current_user
from ..dependencies import db_dependency, run_simulation
from ..helpers import fetch_characters_from_db
from .enemies import get_enemy

router = APIRouter()


@router.post(
    "/simulation", response_model=SimData, status_code=status.HTTP_200_OK
)
def initialize_simulation(
    request: SimRequest,
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
):
    players = []
    characters = fetch_characters_from_db(current_user, db).characters
    for character in characters:
        players.append(convert_to_player_dict(character))

    enemies = []
    for enemy in request.enemies:
        db_enemy = get_enemy(enemy.id, db)
        enemy_dict = convert_to_enemy_dict(db_enemy)
        for i in range(enemy.quantity):
            enemies.append(enemy_dict)

    winner = run_simulation(players, enemies)

    response = {"winner": winner}

    return response


def convert_to_player_dict(character: Character):
    defense_dict = {
        "armor_class": character.defenses.armor_class,
        "saves": {
            "fortitude": character.defenses.saves.fortitude,
            "reflex": character.defenses.saves.reflex,
            "will": character.defenses.saves.will,
        },
    }
    actions_dict = {"attacks": []}
    if character.actions.attacks:
        for attack in character.actions.attacks:
            attack_dict = {
                "name": attack.name,
                "attackBonus": attack.attackBonus,
                "damage": attack.damage,
                "damageType": attack.damageType,
            }
            actions_dict["attacks"].append(attack_dict)

    player_dict = {
        "name": character.name,
        "level": character.level,
        "perception": character.perception,
        "max_hit_points": character.max_hit_points,
        "speed": character.speed,
        "skills": dict(character.skills),
        "attribute_modifiers": dict(character.attribute_modifiers),
        "defenses": defense_dict,
        "actions": actions_dict,
        "ancestry": character.ancestry,
        "class": character.class_,
    }

    return player_dict


def convert_to_enemy_dict(enemy: Enemy):
    enemy_dict = {
        "name": enemy.name,
        "level": enemy.level,
        "perception": enemy.perception,
        "max_hit_points": enemy.max_hit_points,
        "speed": enemy.speed,
        "skills": enemy.skills,
        "attribute_modifiers": enemy.attribute_modifiers,
        "defenses": enemy.defenses,
        "actions": enemy.actions,
        "traits": enemy.traits,
        "immunities": enemy.immunities,
    }

    return enemy_dict
