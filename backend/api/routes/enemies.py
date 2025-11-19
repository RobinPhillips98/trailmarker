"""Functions for API calls related to enemies

Defines functions that are called when a request is made to the /enemies
route of the API, including creating and reading enemies.

"""

import os
from pathlib import Path

import requests
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select

import models
from schemas import Enemies, Enemy, EnemyCreate

from ..dependencies import db_dependency

router = APIRouter()


@router.get("/enemies", response_model=Enemies, status_code=status.HTTP_200_OK)
def get_enemies(db: db_dependency) -> Enemies:
    """Fetches all enemies from the database.

    Args:
        db (db_dependency): A SQLAlchemy database session

    Returns:
        Enemies: A list of enemy objects
    """
    first_row = db.query(models.Enemy).first()
    if not first_row:
        post_enemies()
    query = select(models.Enemy)
    result = db.execute(query)
    enemies = result.scalars().all()
    enemy_list = [e.__dict__ for e in enemies]
    return Enemies(enemies=enemy_list)


@router.get(
    "/enemies/{enemy_id}", response_model=Enemy, status_code=status.HTTP_200_OK
)
def get_enemy(enemy_id: int, db: db_dependency) -> Enemy:
    """Fetches a specific enemy from the database

    Args:
        enemy_id (int): The ID of the enemy to be fetched
        db (db_dependency): A SQLAlchemy database session

    Returns:
        Enemy: A dictionary representing an enemy
    """

    query = db.query(models.Enemy).where(models.Enemy.id == enemy_id)

    result = db.execute(query)
    enemy = result.scalars().first()

    return enemy


# TODO Replace methods below by having initialize_data directly add enemies
# to the databse
@router.post(
    "/enemies", response_model=Enemy, status_code=status.HTTP_201_CREATED
)
async def add_enemy(enemy: EnemyCreate, db: db_dependency) -> Enemy:
    """Adds a given enemy to the database

    Args:
        enemy (EnemyCreate): The enemy to be added to the database
        db (db_dependency): A SQLAlchemy database session

    Raises:
        http_err: A caught HTTP error
        HTTPException: A non-HTTP exception caught and raised as an HTTP 500
            exception

    Returns:
        Enemy: The enemy that was just created.
    """
    try:
        db_enemy = convert_to_db_enemy(enemy)

        db.add(db_enemy)
        db.commit()
        db.refresh(db_enemy)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in add_enemy: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        )
    return db_enemy


def convert_to_db_enemy(enemy: EnemyCreate) -> models.Enemy:
    """Reformats a given enemy to match the model used by the database

    Args:
        enemy (EnemyCreate): The enemy being converted
        user (models.User): The user the enemy should belong to.

    Returns:
        models.Enemy: A representation of the enemy ready to be added to
            the database.
    """
    defense_dict = {
        "armor_class": enemy.defenses.armor_class,
        "saves": {
            "fortitude": enemy.defenses.saves.fortitude,
            "reflex": enemy.defenses.saves.reflex,
            "will": enemy.defenses.saves.will,
        },
    }
    actions_dict = {"attacks": []}
    for attack in enemy.actions.attacks:
        attack_dict = {
            "name": attack.name,
            "attackBonus": attack.attackBonus,
            "damage": attack.damage,
            "damageType": attack.damageType,
        }
        actions_dict["attacks"].append(attack_dict)

    db_enemy = models.Enemy(
        name=enemy.name,
        level=enemy.level,
        traits=enemy.traits,
        perception=enemy.perception,
        skills=dict(enemy.skills),
        attribute_modifiers=dict(enemy.attribute_modifiers),
        defenses=defense_dict,
        max_hit_points=enemy.max_hit_points,
        immunities=enemy.immunities,
        speed=enemy.speed,
        actions=actions_dict,
    )

    return db_enemy


def post_enemies():
    root_directory = str(Path(__file__).parent.parent.parent)
    bestiary_path = f"{root_directory}/data/bestiary/"
    url = "http://localhost:8000/enemies"

    files = os.listdir(bestiary_path)
    files.sort()
    for file in files:
        path = Path(f"{bestiary_path}{file}")
        data = path.read_text()
        requests.post(url, data)
