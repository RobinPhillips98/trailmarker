"""Functions for API calls related to characters

Defines functions that are called when a request is made to the /characters
route of the API including creating, reading, updating, and deleting characters

"""

import logging
from types import SimpleNamespace

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import models
from api.auth_helpers import get_current_user
from api.creature_helpers import (
    build_attack_list,
    build_spell_list,
    convert_to_db_character,
    fetch_characters_from_db,
)
from api.exceptions import (
    ForbiddenException,
    InternalServerError,
    NotFoundException,
)
from api.import_helpers import convert_import_to_character
from db import get_db
from schemas import (
    Attributes,
    BasicResponse,
    Character,
    CharacterCreate,
    CharacterUpdate,
    PathbuilderImport,
)

router = APIRouter(prefix="/characters", tags=["characters"])
logger = logging.getLogger(__name__)


@router.get(
    "/", response_model=list[Character], status_code=status.HTTP_200_OK
)
async def get_characters(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> list[Character]:
    """Fetches all characters owned by the current user

    Args:
        db (AsyncSession): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Returns:
        list[Character]: A list of Character objects
    """
    try:
        return await fetch_characters_from_db(current_user, db)
    except Exception:
        logger.exception("Error in get_characters")
        raise InternalServerError()


@router.get(
    "/{character_id}", response_model=Character, status_code=status.HTTP_200_OK
)
async def get_character(
    character_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Character:
    """Fetches a character by ID

    Args:
        character_id (int): The ID of the character to be fetched
        db (AsyncSession): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        NotFoundException: A 404 exception if the character is not found.
        ForbiddenException: A 403 exception if the character does not
            belong to the current user
        InternalServerError: A non-HTTP exception caught and raised as an HTTP
            500 exception
    Returns:
        Character: The character object matching `character_id`
    """
    try:
        character = await db.get(models.Character, character_id)

        if character is None:
            raise NotFoundException(route="character")

        if character.user_id != current_user.id:
            raise ForbiddenException(action="view", route="character")

        return character
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error in get_character")
        raise InternalServerError()


@router.post(
    "/", response_model=Character, status_code=status.HTTP_201_CREATED
)
async def add_character(
    character: CharacterCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Character:
    """Adds `character` to the database, attached to `current_user`

    Args:
        character (CharacterCreate): The character to be added to the database
        db (AsyncSession): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
            Defaults to Depends(get_current_user).

    Raises:
        BadRequestException: On a duplicate character name for the same user.
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
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error in add_character")
        raise InternalServerError()
    return db_character


@router.post(
    "/import",
    response_model=Character,
    status_code=status.HTTP_201_CREATED,
)
async def import_character(
    imported_character: PathbuilderImport,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Character:
    """Adds a character imported from Pathbuilder to the database

    Reads a JSON file from Pathbuilder, converts it to the character format
    used by Trailmarker, then adds the character to the database as normal.

    Args:
        imported_character (PathbuilderImport): An exported JSON file from
            Pathbuilder2e representing a Pathfinder 2E character
        db (AsyncSession): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        BadRequestException: On a duplicate character name for the same user.
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
    except HTTPException:
        raise
    except Exception:
        logger.exception("Error in import_character")
        raise InternalServerError()
    return db_character


@router.patch(
    "/{character_id}", response_model=Character, status_code=status.HTTP_200_OK
)
async def update_character(
    character_id: int,
    character_update: CharacterUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Character:
    """Updates a given character in the database.

    Uses `character_id` to fetch a character from the database and then uses
    `character_update` to overwrite that character's data with the data
    provided in `character_update`. Only fields included in the request will be
    updated - all other fields will be left as they are.

    Args:
        character_id (int): The ID of the character to be updated.
        character_update (CharacterUpdate): A dictionary containing the data to
            be added or changes for the character.
        db (AsyncSession): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        NotFoundException: A 404 exception if the character is not found.
        ForbiddenException: A 403 exception if the character does not
            belong to the current user
        InternalServerError: A non-HTTP exception caught and raised as an HTTP
            500 exception

    Returns:
        Character: The updated character's data
    """
    try:
        db_character = await db.get(models.Character, character_id)

        if db_character is None:
            raise NotFoundException(route="character")

        if db_character.user_id != current_user.id:
            raise ForbiddenException(action="update", route="character")

        update_data = character_update.model_dump(exclude_unset=True)

        if character_update.actions:
            # Need to fill in values needed by build_attack_list and
            # build_spell_list that aren't included in the update_data
            effective_character_data = SimpleNamespace(
                actions=character_update.actions,
                level=(
                    character_update.level
                    if character_update.level is not None
                    else db_character.level
                ),
                attribute_modifiers=(
                    character_update.attribute_modifiers
                    if character_update.attribute_modifiers is not None
                    else Attributes.model_validate(
                        db_character.attribute_modifiers
                    )
                ),
                proficiencies=(
                    character_update.proficiencies
                    if "proficiencies" in update_data
                    else db_character.proficiencies
                ),
                extra_proficiencies=(
                    character_update.extra_proficiencies
                    if "extra_proficiencies" in update_data
                    else db_character.extra_proficiencies
                ),
                other_features=(
                    character_update.other_features
                    if "other_features" in update_data
                    else db_character.other_features
                ),
            )
            if character_update.actions.attacks is not None:
                update_data["actions"]["attacks"] = build_attack_list(
                    effective_character_data
                )
            if character_update.actions.spells is not None:
                update_data["actions"]["spells"] = build_spell_list(
                    effective_character_data
                )

        for key, value in update_data.items():
            setattr(db_character, key, value)

        await db.commit()
        await db.refresh(db_character)

        updated_character = Character.model_validate(db_character)
        return updated_character

    except HTTPException:
        raise
    except Exception:
        logger.exception("Error in update_character")
        raise InternalServerError()


@router.delete(
    "/{character_id}",
    response_model=BasicResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_character(
    character_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> BasicResponse:
    """Fetches a character by ID and deletes it from the database

    Args:
        character_id (int): The ID of the character to be deleted
        db (AsyncSession): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        NotFoundException: A 404 exception if the character is not found.
        ForbiddenException: A 403 exception if the character does not
            belong to the current user

    Returns:
        BasicResponse: A response object confirming the character was deleted.
    """
    character = await db.get(models.Character, character_id)

    if not character:
        raise NotFoundException(route="character")

    if character.user_id != current_user.id:
        raise ForbiddenException(action="delete", route="character")

    await db.delete(character)
    await db.commit()

    return {"message": "Character deleted"}
