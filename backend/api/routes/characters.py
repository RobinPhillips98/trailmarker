"""Functions for API calls related to characters

Defines functions that are called when a request is made to the /characters
route of the API including creating, reading, updating, and deleting characters

"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

import models
from schemas import (
    BasicResponse,
    Character,
    CharacterCreate,
    Characters,
    CharacterUpdate,
    PathbuilderImport,
)

from ..auth_helpers import get_current_user
from ..character_helpers import (
    build_attack_list,
    build_spell_list,
    convert_to_db_character,
    fetch_characters_from_db,
)
from ..dependencies import db_dependency
from ..exceptions import (
    ForbiddenException,
    InternalServerError,
    NotFoundException,
)
from ..import_helpers import convert_import_to_character

router = APIRouter()


@router.get(
    "/characters", response_model=Characters, status_code=status.HTTP_200_OK
)
async def get_characters(
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> Characters:
    """Fetches all characters owned by the current user

    Args:
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Returns:
        Characters: A list of Character objects
    """
    try:
        return await fetch_characters_from_db(current_user, db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in get_characters: {str(e)}")
        raise InternalServerError(message=str(e))


@router.post(
    "/characters",
    response_model=Character,
    status_code=status.HTTP_201_CREATED,
)
async def add_character(
    character: CharacterCreate,
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> Character:
    """Adds `character` to the database, attached to `current_user`

    Args:
        character (CharacterCreate): The character to be added to the database
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        http_err: A caught HTTP error
        InternalServerError: A non-HTTP exception caught and raised as an HTTP
            500 exception

    Returns:
        Character: The character added to the database
    """
    try:
        db_character = convert_to_db_character(character, current_user)

        db.add(db_character)
        await db.commit()
        await db.refresh(db_character)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in add_character: {str(e)}")
        raise InternalServerError(message=str(e))
    return db_character


@router.post(
    "/characters/import",
    response_model=Character,
    status_code=status.HTTP_200_OK,
)
async def import_character(
    imported_character: PathbuilderImport,
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> Character:
    """Adds a character imported from Pathbuilder to the database

    Reads a JSON file from Pathbuilder, converts it to the character format
    used by Trailmarker, then adds the character to the database as normal.

    Args:
        imported_character (PathbuilderImport): An exported JSON file from
            Pathbuilder2e representing a Pathfinder 2E character
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        http_err: A caught HTTP error
        InternalServerError: A non-HTTP exception caught and raised as an HTTP
            500 exception

    Returns:
        Character: The character added to the database
    """
    try:
        converted_character = convert_import_to_character(imported_character)

        db_character = convert_to_db_character(
            converted_character, current_user
        )

        db.add(db_character)
        await db.commit()
        await db.refresh(db_character)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in add_character: {str(e)}")
        raise InternalServerError(message=str(e))
    return db_character


@router.patch(
    "/characters", response_model=Character, status_code=status.HTTP_200_OK
)
async def update_character(
    character_update: CharacterUpdate,
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> Character:
    """Updates a given character in the database.

    Uses the ID contained in `character_update` to fetch a character from the
    database and then uses the rest of `character_update` to overwrite that
    character's data with the data in `character_update`.

    Args:
        character_update (CharacterUpdate): A dictionary containing the data to
            be added or changes for the character.
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        NotFoundException: A 404 exception if the character is not found.
        ForbiddenException: A 403 exception if the character does not
            belong to the current user
        http_err: A caught HTTP error
        InternalServerError: A non-HTTP exception caught and raised as an HTTP
            500 exception

    Returns:
        Character: The updated character's data
    """
    try:
        db_character = await db.get(models.Character, character_update.id)

        if db_character is None:
            raise NotFoundException(route="character")

        if db_character.user_id != current_user.id:
            raise ForbiddenException(action="update", route="character")

        update_data = character_update.dict(exclude_unset=True)
        update_data["actions"]["attacks"] = build_attack_list(character_update)
        update_data["actions"]["spells"] = build_spell_list(character_update)

        for key, value in update_data.items():
            setattr(db_character, key, value)

        await db.commit()
        await db.refresh(db_character)

        updated_character = Character.from_orm(db_character)
        return updated_character

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in update_character: {str(e)}")
        raise InternalServerError(message=str(e))


@router.delete(
    "/characters/{character_id}",
    response_model=BasicResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_character(
    character_id: int,
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> object:
    """Fetches a character by ID and deletes it from the database

    Args:
        character_id (int): The ID of the character to be deleted
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        NotFoundException: A 404 exception if the character is not found.
        ForbiddenException: A 403 exception if the character does not
            belong to the current user

    Returns:
        object: A response object confirming the character was deleted.
    """
    stmt = (
        select(models.Character)
        .options(selectinload(models.Character.user))
        .where(models.Character.id == character_id)
    )

    result = await db.execute(stmt)
    character = result.scalar_one_or_none()

    if not character:
        raise NotFoundException(route="character")

    if character.user_id != current_user.id:
        raise ForbiddenException(action="delete", route="character")

    await db.delete(character)
    await db.commit()

    return {"message": "Character deleted"}
