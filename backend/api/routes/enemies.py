"""Functions for API calls related to enemies

Defines functions that are called when a request is made to the /enemies
route of the API, including reading enemies.

"""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select

import models
from api.exceptions import InternalServerError, NotFoundException
from schemas import BasicResponse, Enemy, EnemyCreate, EnemyUpdate

from ..dependencies import db_dependency

router = APIRouter(prefix="/enemies", tags=["enemies"])


@router.get("/", response_model=list[Enemy], status_code=status.HTTP_200_OK)
async def get_enemies(db: db_dependency) -> list[Enemy]:
    """Fetches all enemies from the database.

    Args:
        db (db_dependency): A SQLAlchemy database session

    Returns:
        list[Enemy]: A list of enemy objects
    """
    try:
        stmt = select(models.Enemy)
        enemies = (await db.scalars(stmt)).all()
        return enemies
    except Exception as e:
        print(f"Error in get_enemies: {str(e)}")
        raise InternalServerError("An error occurred while fetching enemies")


@router.get(
    "/{enemy_id}", response_model=Enemy, status_code=status.HTTP_200_OK
)
async def get_enemy(enemy_id: int, db: db_dependency) -> Enemy:
    """Fetches the enemy with ID `enemy_id` from the database

    Args:
        enemy_id (int): The ID of the enemy to be fetched
        db (db_dependency): A SQLAlchemy database session

    Returns:
        Enemy: An ORM model representing an enemy
    """
    try:
        enemy = await db.get(models.Enemy, enemy_id)
        if not enemy:
            raise NotFoundException("Enemy not found")
        return enemy
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in get_enemy: {str(e)}")
        raise InternalServerError("An error occurred while fetching the enemy")


@router.post("/", response_model=Enemy, status_code=status.HTTP_201_CREATED)
async def create_enemy(enemy: EnemyCreate, db: db_dependency) -> Enemy:
    """Creates a new enemy in the database.

    Args:
        enemy (EnemyCreate): An EnemyCreate object containing the data for the
            new enemy
        db (db_dependency): A SQLAlchemy database session

    Returns:
        Enemy: The newly created enemy object
    """
    try:
        db_enemy = models.Enemy(
            name=enemy.name,
            level=enemy.level,
            perception=enemy.perception,
            skills=enemy.skills,
            attribute_modifiers=enemy.attribute_modifiers,
            defenses=enemy.defenses,
            max_hit_points=enemy.max_hit_points,
            spell_attack_bonus=enemy.spell_attack_bonus,
            spell_dc=enemy.spell_dc,
            speed=enemy.speed,
            actions=enemy.actions,
            traits=enemy.traits,
            immunities=enemy.immunities,
            weaknesses=enemy.weaknesses,
            resistances=enemy.resistances,
        )
        db.add(db_enemy)
        await db.commit()
        await db.refresh(db_enemy)

        created_enemy = Enemy.model_validate(db_enemy)
        return created_enemy
    except Exception as e:
        print(f"Error in create_enemy: {str(e)}")
        raise InternalServerError("An error occurred while creating the enemy")


@router.patch(
    "/{enemy_id}", response_model=Enemy, status_code=status.HTTP_200_OK
)
async def update_enemy(
    enemy_id: int, enemy_update: EnemyUpdate, db: db_dependency
) -> Enemy:
    """Updates the enemy with ID `enemy_id` in the database with the data in
    `enemy_update`.

    Args:
        enemy_id (int): The ID of the enemy to be updated.
        enemy_update (EnemyUpdate): An EnemyUpdate object containing the data
            to be added or changes for the enemy.
        db (db_dependency): A SQLAlchemy database session

    Raises:
        NotFoundException: If no enemy with ID `enemy_id` is found in the
            database.
        InternalServerError: If an error occurs while updating the enemy.
    """
    try:
        db_enemy = await db.get(models.Enemy, enemy_id)
        if not db_enemy:
            raise NotFoundException("Enemy not found")

        update_data = enemy_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_enemy, key, value)

        db.add(db_enemy)
        await db.commit()
        await db.refresh(db_enemy)

        updated_enemy = Enemy.model_validate(db_enemy)
        return updated_enemy
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in update_enemy: {str(e)}")
        raise InternalServerError("An error occurred while updating the enemy")


@router.delete(
    "/{enemy_id}",
    response_model=BasicResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_enemy(
    enemy_id: int,
    db: db_dependency,
) -> BasicResponse:
    """Fetches an enemy by ID and deletes it from the database

    Args:
        enemy_id (int): The ID of the enemy to be deleted
        db (db_dependency): A SQLAlchemy database session

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
            raise NotFoundException("Enemy not found")

        await db.delete(enemy)
        await db.commit()

        return {"message": "Enemy deleted successfully"}
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in delete_enemy: {str(e)}")
        raise InternalServerError("An error occurred while deleting the enemy")
