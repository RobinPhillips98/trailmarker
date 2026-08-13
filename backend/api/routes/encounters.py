"""Functions for API calls related to saved encounters

Defines functions that are called when a request is made to the /encounters
route of the API, including creating, reading, and deleting encounters.

"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
from api.auth_helpers import get_current_user
from api.exceptions import (
    ForbiddenException,
    InternalServerError,
    NotFoundException,
)
from db import get_db
from schemas import BasicResponse, Encounter, EncounterCreate, EncounterUpdate

router = APIRouter(prefix="/encounters", tags=["encounters"])
logger = logging.getLogger(__name__)


@router.get(
    "/", response_model=list[Encounter], status_code=status.HTTP_200_OK
)
async def get_encounters(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> list[Encounter]:
    """Fetches all encounters owned by the current user

    Args:
        db (AsyncSession): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        InternalServerError: A non-HTTP exception caught and raised as an HTTP
            500 exception

    Returns:
        list[Encounter]: A list of encounter objects
    """
    try:
        stmt = select(models.Encounter).where(
            models.Encounter.user_id == current_user.id
        )
        encounters = (await db.scalars(stmt)).all()
        return encounters
    except Exception:
        logger.exception("Error in get_encounters")
        raise InternalServerError()


@router.get(
    "/{encounter_id}", response_model=Encounter, status_code=status.HTTP_200_OK
)
async def get_encounter(
    encounter_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Encounter:
    """Fetches an encounter by ID

    Args:
        encounter_id (int): The ID of the encounter to be fetched
        db (AsyncSession): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        NotFoundException: A 404 exception if the encounter is not found.
        ForbiddenException: A 403 exception if the encounter does not
            belong to the current user
        InternalServerError: A non-HTTP exception caught and raised as an HTTP
            500 exception
    Returns:
        Encounter: The encounter with the specified ID
    """
    try:
        encounter = await db.get(models.Encounter, encounter_id)

        if not encounter:
            raise NotFoundException(route="encounter")

        if encounter.user_id != current_user.id:
            raise ForbiddenException(action="view", route="encounter")

        return Encounter.model_validate(encounter)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error in get_encounter")
        raise InternalServerError()


@router.post(
    "/", response_model=Encounter, status_code=status.HTTP_201_CREATED
)
async def add_encounter(
    encounter: EncounterCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Encounter:
    """Adds `encounter` to the database

    Args:
        encounter (Encounter): The encounter to be added to the database
        db (AsyncSession): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        InternalServerError: A non-HTTP exception caught and raised as an HTTP
            500 exception

    Returns:
        Encounter: The encounter added to the database
    """
    try:
        db_encounter = models.Encounter(
            name=encounter.name, enemies=encounter.enemies, user=current_user
        )
        db.add(db_encounter)
        await db.commit()
        await db.refresh(db_encounter)

        created_encounter = Encounter.model_validate(db_encounter)
        return created_encounter
    except Exception:
        logger.exception("Error in add_encounter")
        raise InternalServerError()


@router.patch(
    "/{encounter_id}", response_model=Encounter, status_code=status.HTTP_200_OK
)
async def update_encounter(
    encounter_id: int,
    encounter_update: EncounterUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Encounter:
    """Fetches an encounter by ID and updates it with the provided data

    Args:
        encounter_id (int): The ID of the encounter to be updated
        encounter_update (EncounterUpdate): The data used to update the
            encounter
        db (AsyncSession): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        NotFoundException: A 404 exception if the encounter is not found.
        ForbiddenException: A 403 exception if the encounter does not
            belong to the current user
        InternalServerError: A non-HTTP exception caught and raised as an HTTP
            500 exception

    Returns:
        Encounter: The updated encounter object
    """
    try:
        db_encounter = await db.get(models.Encounter, encounter_id)

        if db_encounter is None:
            raise NotFoundException(route="encounter")

        if db_encounter.user_id != current_user.id:
            raise ForbiddenException(action="update", route="encounter")

        update_data = encounter_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_encounter, key, value)

        await db.commit()
        await db.refresh(db_encounter)

        updated_encounter = Encounter.model_validate(db_encounter)
        return updated_encounter
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error in update_encounter")
        raise InternalServerError()


@router.delete(
    "/{encounter_id}",
    response_model=BasicResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_encounter(
    encounter_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> BasicResponse:
    """Fetches an encounter by ID and deletes it from the database

    Args:
        encounter_id (int): The ID of the encounter to be deleted
        db (AsyncSession): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        NotFoundException: A 404 exception if the encounter is not found.
        ForbiddenException: A 403 exception if the encounter does not
            belong to the current user

    Returns:
        BasicResponse: A response object confirming the encounter was deleted.
    """
    encounter = await db.get(models.Encounter, encounter_id)

    if not encounter:
        raise NotFoundException(route="encounter")

    if encounter.user_id != current_user.id:
        raise ForbiddenException(action="delete", route="encounter")

    await db.delete(encounter)
    await db.commit()

    return {"message": "Encounter deleted"}
