"""Functions for API calls related to enemies

Defines functions that are called when a request is made to the /enemies
route of the API, including reading enemies.

"""

from fastapi import APIRouter, status
from sqlalchemy.future import select

import models
from schemas import Enemies, Enemy

from ..dependencies import db_dependency

router = APIRouter()


@router.get("/enemies", response_model=Enemies, status_code=status.HTTP_200_OK)
async def get_enemies(db: db_dependency) -> Enemies:
    """Fetches all enemies from the database.

    Args:
        db (db_dependency): A SQLAlchemy database session

    Returns:
        Enemies: A list of enemy objects
    """
    query = select(models.Enemy)
    result = await db.execute(query)
    enemies = result.scalars().all()
    enemy_list = [e.__dict__ for e in enemies]
    return Enemies(enemies=enemy_list)


@router.get(
    "/enemies/{enemy_id}", response_model=Enemy, status_code=status.HTTP_200_OK
)
async def get_enemy(enemy_id: int, db: db_dependency) -> Enemy:
    """Fetches the enemy with ID `enemy_id` from the database

    Args:
        enemy_id (int): The ID of the enemy to be fetched
        db (db_dependency): A SQLAlchemy database session

    Returns:
        Enemy: An ORM model representing an enemy
    """
    query = select(models.Enemy)
    query = query.where(models.Enemy.id == enemy_id)

    result = await db.execute(query)
    enemy = result.scalars().first()

    return enemy
