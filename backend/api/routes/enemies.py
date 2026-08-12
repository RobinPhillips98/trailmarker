"""Functions for API calls related to enemies

Defines functions that are called when a request is made to the /enemies
route of the API.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
from api.creature_helpers import (
    build_attack_list,
    build_spell_list,
    convert_to_db_enemy,
)
from api.exceptions import InternalServerError, NotFoundException
from db import get_db
from schemas import BasicResponse, Enemy, EnemyCreate, EnemyUpdate

router = APIRouter(prefix="/enemies", tags=["enemies"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[Enemy], status_code=status.HTTP_200_OK)
async def get_enemies(db: AsyncSession = Depends(get_db)) -> list[Enemy]:
    """Fetches all enemies from the database.

    Args:
        db (AsyncSession): A SQLAlchemy database session

    Returns:
        list[Enemy]: A list of enemy objects
    """
    try:
        stmt = select(models.Enemy).order_by(models.Enemy.name)
        enemies = (await db.scalars(stmt)).all()
        return enemies
    except Exception:
        logger.exception("Error in get_enemies")
        raise InternalServerError()


@router.get(
    "/{enemy_id}", response_model=Enemy, status_code=status.HTTP_200_OK
)
async def get_enemy(
    enemy_id: int, db: AsyncSession = Depends(get_db)
) -> Enemy:
    """Fetches the enemy with ID `enemy_id` from the database

    Args:
        enemy_id (int): The ID of the enemy to be fetched
        db (AsyncSession): A SQLAlchemy database session

    Returns:
        Enemy: An ORM model representing an enemy
    """
    try:
        enemy = await db.get(models.Enemy, enemy_id)
        if not enemy:
            raise NotFoundException("Enemy")
        return enemy
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error in get_enemy")
        raise InternalServerError()


@router.post("/", response_model=Enemy, status_code=status.HTTP_201_CREATED)
async def create_enemy(
    enemy: EnemyCreate, db: AsyncSession = Depends(get_db)
) -> Enemy:
    """Creates a new enemy in the database.

    Args:
        enemy (EnemyCreate): An EnemyCreate object containing the data for the
            new enemy
        db (AsyncSession): A SQLAlchemy database session

    Returns:
        Enemy: The newly created enemy object
    """
    try:
        db_enemy = convert_to_db_enemy(enemy)
        db.add(db_enemy)
        await db.commit()
        await db.refresh(db_enemy)

        created_enemy = Enemy.model_validate(db_enemy)
        return created_enemy
    except Exception:
        logger.exception("Error in create_enemy")
        raise InternalServerError()


@router.patch(
    "/{enemy_id}", response_model=Enemy, status_code=status.HTTP_200_OK
)
async def update_enemy(
    enemy_id: int,
    enemy_update: EnemyUpdate,
    db: AsyncSession = Depends(get_db),
) -> Enemy:
    """Updates the enemy with ID `enemy_id` in the database with the data in
    `enemy_update`.

    Args:
        enemy_id (int): The ID of the enemy to be updated.
        enemy_update (EnemyUpdate): An EnemyUpdate object containing the data
            to be added or changes for the enemy.
        db (AsyncSession): A SQLAlchemy database session

    Raises:
        NotFoundException: If no enemy with ID `enemy_id` is found in the
            database.
        InternalServerError: If an error occurs while updating the enemy.
    """
    try:
        db_enemy = await db.get(models.Enemy, enemy_id)
        if not db_enemy:
            raise NotFoundException("Enemy")

        update_data = enemy_update.model_dump(exclude_unset=True)
        update_data["actions"]["attacks"] = build_attack_list(enemy_update)
        update_data["actions"]["spells"] = build_spell_list(enemy_update)
        for key, value in update_data.items():
            setattr(db_enemy, key, value)

        await db.commit()
        await db.refresh(db_enemy)

        updated_enemy = Enemy.model_validate(db_enemy)
        return updated_enemy
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error in update_enemy")
        raise InternalServerError()


@router.delete(
    "/{enemy_id}",
    response_model=BasicResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_enemy(
    enemy_id: int,
    db: AsyncSession = Depends(get_db),
) -> BasicResponse:
    """Fetches an enemy by ID and deletes it from the database

    Args:
        enemy_id (int): The ID of the enemy to be deleted
        db (AsyncSession): A SQLAlchemy database session

    Raises:
        NotFoundException: If no enemy with ID `enemy_id` is found in the
            database.
        InternalServerError: If an error occurs while deleting the enemy.

    Returns:
        BasicResponse: A response object confirming the enemy was deleted.
    """
    try:
        enemy = await db.get(models.Enemy, enemy_id)
        if not enemy:
            raise NotFoundException("Enemy")

        await db.delete(enemy)
        await db.commit()

        return {"message": "Enemy deleted successfully."}
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error in delete_enemy")
        raise InternalServerError()
