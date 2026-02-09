from fastapi import APIRouter, Depends, status

import models
from schemas import Character, Enemy, SimRequest, SimResponse

from ..auth_helpers import get_current_user
from ..dependencies import db_dependency, run_simulation
from ..helpers import fetch_characters_from_db
from .enemies import get_enemy

router = APIRouter()


@router.post(
    "/simulation", response_model=SimResponse, status_code=status.HTTP_200_OK
)
def run_simulations(
    request: SimRequest,
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> SimResponse:
    """Runs simulations using current user's party and requested enemies.

    Takes in a list of enemy IDs and quantities, then fetches all player
    characters associated with the current user as well as the enemies whose
    IDs were passed in and creates a list of each, then runs a number of
    simulations and returns a response with data from those simulations.

    Args:
        request (SimRequest): List of enemy IDs and the quantity of each enemy.
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Returns:
        SimResponse: Number of simulations won and data from each simulation.
    """
    total_sims = 100
    response = {"wins": 0, "total_sims": total_sims, "sim_data": []}
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

    # print("Running simulations...")
    for i in range(total_sims):
        # print(f"Running simulation {i + 1}...")
        sim_data = run_simulation(players, enemies)
        if sim_data["winner"] == "players":
            response["wins"] += 1
        response["sim_data"].append(sim_data)
    # print("Simulations complete. Sending response...")

    return response


def convert_to_player_dict(character: Character) -> dict[str, any]:
    """Returns a reformatted dictionary using the given character object.

    Args:
        character (Character): The Character object to be converted.

    Returns:
        dict[str, any]: Dictionary formatted for use by the simulation.
    """
    defense_dict = {
        "armor_class": character.defenses.armor_class,
        "saves": {
            "fortitude": character.defenses.saves.fortitude,
            "reflex": character.defenses.saves.reflex,
            "will": character.defenses.saves.will,
        },
    }
    actions_dict = {"attacks": [], "spells": []}
    if character.actions.attacks:
        for attack in character.actions.attacks:
            attack_dict = {
                "name": attack.name,
                "attackBonus": attack.attackBonus,
                "damage": attack.damage,
                "damageType": attack.damageType,
            }
            actions_dict["attacks"].append(attack_dict)
    if character.actions.spells:
        for spell in character.actions.spells:
            spell_dict = {
                "name": spell.name,
                "slots": spell.slots,
                "level": spell.level,
                "damage_roll": spell.damage_roll,
                "damage_type": spell.damage_type,
                "range": spell.range_,
                "area": spell.area,
                "save": spell.save,
                "target": spell.target,
                "actions": spell.actions,
            }
            actions_dict["spells"].append(spell_dict)

    player_dict = {
        "name": character.name,
        "level": character.level,
        "perception": character.perception,
        "max_hit_points": character.max_hit_points,
        "spell_attack_bonus": character.spell_attack_bonus,
        "spell_dc": character.spell_dc,
        "speed": character.speed,
        "skills": dict(character.skills),
        "attribute_modifiers": dict(character.attribute_modifiers),
        "defenses": defense_dict,
        "actions": actions_dict,
        "ancestry": character.ancestry,
        "class": character.class_,
    }

    return player_dict


def convert_to_enemy_dict(enemy: Enemy) -> dict[str, any]:
    """Returns a reformatted dictionary using the given enemy object.

    Args:
        enemy (Enemy): The Enemy object to be converted.

    Returns:
        dict[str, any]: Dictionary formatted for use by the simulation.
    """
    enemy_dict = {
        "name": enemy.name,
        "level": enemy.level,
        "perception": enemy.perception,
        "max_hit_points": enemy.max_hit_points,
        "spell_attack_bonus": enemy.spell_attack_bonus,
        "spell_dc": enemy.spell_dc,
        "speed": enemy.speed,
        "skills": enemy.skills,
        "attribute_modifiers": enemy.attribute_modifiers,
        "defenses": enemy.defenses,
        "actions": enemy.actions,
        "traits": enemy.traits,
        "immunities": enemy.immunities,
    }

    return enemy_dict
