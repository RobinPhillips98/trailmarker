"""Functions for API calls related to encounters

Defines functions that are called when a request is made to the /encounters
route of the API, including creating, reading, and deleting encounters.

"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

import models
from schemas import Encounter, Encounters

from ..auth_helpers import get_current_user
from ..dependencies import db_dependency
from ..exceptions import NotAuthorizedException, NotFoundException

router = APIRouter()


@router.get(
    "/encounters", response_model=Encounters, status_code=status.HTTP_200_OK
)
async def get_encounters(
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> Encounters:
    """Fetches all encounters owned by the current user

    Args:
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Returns:
        Encounters: A list of encounter objects
    """
    query = select(models.Encounter).options(
        selectinload(models.Encounter.user)
    )
    query = query.where(models.Encounter.user_id == current_user.id)
    result = await db.execute(query)
    encounters = result.scalars().all()
    encounter_list = [e.__dict__ for e in encounters]
    return Encounters(encounters=encounter_list)


@router.post(
    "/encounters",
    response_model=Encounter,
    status_code=status.HTTP_201_CREATED,
)
async def add_encounter(
    encounter: Encounter,
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> Encounter:
    """Adds the given encounter to the database

    Args:
        encounter (EncounterCreate): The encounter to be added to the database
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        http_err: A caught HTTP error
        HTTPException: A non-HTTP exception caught and raised as an HTTP 500
            exception

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
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in add_enemy: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        )
    return db_encounter


@router.delete(
    "/encounters/{encounter_id}",
    response_model=object,
    status_code=status.HTTP_200_OK,
)
async def delete_encounter(
    encounter_id: int,
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> object:
    """Fetches an encounter by ID and deletes it from the database

    Args:
        encounter_id (int): The ID of the encounter to be deleted
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        NotFoundException: A 404 exception if the encounter is not found.
        NotAuthorizedException: A 403 exception if the encounter does not
            belong to the current user

    Returns:
        object: A response object confirming the encounter was deleted.
    """
    stmt = (
        select(models.Encounter)
        .options(selectinload(models.Encounter.user))
        .where(models.Encounter.id == encounter_id)
    )

    result = await db.execute(stmt)
    encounter = result.scalar_one_or_none()

    if not encounter:
        raise NotFoundException(route="encounter")

    if encounter.user_id != current_user.id:
        raise NotAuthorizedException(action="delete", route="encounter")

    await db.delete(encounter)
    await db.commit()

    return {"message": "Encounter deleted"}
