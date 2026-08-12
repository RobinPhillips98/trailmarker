"""Functions for the API call that runs the simulation.

Defines functions used to run the simulation. Namely, a POST request with the
enemies for the simulation that gets the current user's characters, fetches the
enemies from the database, and creates a number of simulation objects, runs a
simulation for each, and returns data from each simulation as well as overall
stats about the simulations.

"""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import models
from api.auth_helpers import get_current_user
from api.creature_helpers import fetch_characters_from_db
from api.exceptions import InternalServerError
from db import get_db
from schemas import Character, Enemy, SimRequest, SimResponse
from simulation.core.simulation import run_simulation

router = APIRouter(prefix="/simulation", tags=["simulation"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=SimResponse, status_code=status.HTTP_200_OK)
async def init_sim_with_auth(
    request: SimRequest,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> SimResponse:
    """Runs simulations using current user's party and requested enemies.

    Takes in a list of enemy IDs and quantities, then fetches all player
    characters associated with the current user as well as the enemies whose
    IDs were passed in and creates a list of each, then runs a number of
    simulations and returns a response with data from those simulations.

    Args:
        request (SimRequest): List of enemy IDs and the quantity of each enemy.
        db (AsyncSession): A SQLAlchemy database session.
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        InternalServerError: Any other caught exception, raised as an HTTP 500
            error.

    Returns:
        SimResponse: Overall data and data from each simulation.
    """
    try:
        return await run_simulations(current_user, request, db)

    except HTTPException:
        raise
    except Exception:
        logger.exception("Error in init_sim_with_auth")
        raise InternalServerError()


@router.post(
    "/pregen",
    response_model=SimResponse,
    status_code=status.HTTP_200_OK,
)
async def init_sim_with_pregens(
    request: SimRequest,
    db: AsyncSession = Depends(get_db),
) -> SimResponse:
    """Runs simulations using a pre-made party and requested enemies.

    Takes in a list of enemy IDs and quantities, then fetches all player
    characters associated with the admin user as well as the enemies whose
    IDs were passed in and creates a list of each, then runs a number of
    simulations and returns a response with data from those simulations.

    Uses the admin user to run the simulation using a pre-generated party.

    Args:
        request (SimRequest): List of enemy IDs and the quantity of each enemy.
        db (AsyncSession): A SQLAlchemy database session.

    Raises:
        InternalServerError: Any other caught exception, raised as an HTTP 500
            error.

    Returns:
        SimResponse: Overall data and data from each simulation.
    """
    try:
        # Admin user with pregens has ID of 1
        user = await db.get(models.User, 1)
        return await run_simulations(user, request, db)

    except HTTPException:
        raise
    except Exception:
        logger.exception("Error in init_sim_with_pregens")
        raise InternalServerError()


async def run_simulations(
    user: models.User, request: SimRequest, db: AsyncSession = Depends(get_db)
) -> SimResponse:
    """Driver to handle running the simulation using the passed in `user`.

    Args:
        user (models.User): The user whose characters should be used.
        request (SimRequest): List of enemy IDs and the quantity of each enemy.
        db (AsyncSession): A SQLAlchemy database session.

    Returns:
        SimResponse: Overall data and data from each simulation.
    """
    total_sims = 100
    response = {
        "total_sims": total_sims,
        "wins": 0,
        "wins_ratio": 0.0,
        "average_deaths": 0.0,
        "average_rounds": 0.0,
        "sim_data": [],
    }
    players = []
    result = await fetch_characters_from_db(user, db)
    characters = [Character.model_validate(character) for character in result]
    for character in characters:
        players.append(convert_to_player_dict(character))

    enemies = []
    for enemy in request.enemies:
        db_enemy = await db.get(models.Enemy, enemy.id)
        if not db_enemy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Enemy with ID {enemy.id} not found",
            )
        enemy_dict = convert_to_enemy_dict(db_enemy)
        for i in range(enemy.quantity):
            enemies.append(enemy_dict)

    for i in range(total_sims):
        sim_data = run_simulation(players, enemies, request.parameters)
        sim_data["sim_num"] = i + 1
        if sim_data["winner"] == "players":
            response["wins"] += 1
        response["sim_data"].append(sim_data)

    response["wins_ratio"] = (response["wins"] / total_sims) * 100

    deaths = sum(data["players_killed"] for data in response["sim_data"])
    response["average_deaths"] = deaths / total_sims

    total_rounds = sum(data["rounds"] for data in response["sim_data"])
    response["average_rounds"] = total_rounds / total_sims

    return SimResponse.model_validate(response)


def convert_to_player_dict(character: Character) -> dict[str, Any]:
    """Returns a reformatted dictionary using `character`.

    Args:
        character (Character): The Character object to be converted.

    Returns:
        dict[str, Any]: Dictionary formatted for use by the simulation.
    """
    defense_dict = {
        "armor_class": character.defenses.armor_class,
        "saves": {
            "fortitude": character.defenses.saves.fortitude,
            "reflex": character.defenses.saves.reflex,
            "will": character.defenses.saves.will,
        },
    }
    actions_dict = {
        "attacks": [],
        "spells": [],
        "heals": character.actions.heals,
        "shield": character.actions.shield,
    }
    if character.actions.attacks:
        for attack in character.actions.attacks:
            attack_dict = {
                "name": attack.name,
                "attackBonus": attack.attackBonus,
                "damage": attack.damage,
                "damageType": attack.damageType,
                "range": attack.range,
                "traits": attack.traits,
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
                "targets": spell.targets,
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
        "heritage": character.heritage,
        "class": character.class_,
    }

    return player_dict


def convert_to_enemy_dict(enemy: Enemy) -> dict[str, Any]:
    """Returns a reformatted dictionary using `enemy`.

    Args:
        enemy (Enemy): The Enemy object to be converted.

    Returns:
        dict[str, Any]: Dictionary formatted for use by the simulation.
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
        "weaknesses": enemy.weaknesses,
        "resistances": enemy.resistances,
    }

    return enemy_dict
