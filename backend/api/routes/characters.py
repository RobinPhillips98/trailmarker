"""Functions for API calls related to characters

Defines functions that are called when a request is made to the /characters
route of the API including creating, reading, updating, and deleting characters

"""

from fastapi import APIRouter, Depends, HTTPException, status

import models
from schemas import Character, CharacterCreate, Characters, CharacterUpdate

from ..auth_helpers import get_current_user
from ..dependencies import db_dependency
from ..exceptions import NotAuthorizedException, NotFoundException
from ..helpers import fetch_characters_from_db

router = APIRouter()


@router.get(
    "/characters", response_model=Characters, status_code=status.HTTP_200_OK
)
def get_characters(
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
    return fetch_characters_from_db(current_user, db)


@router.get(
    "/characters/{character_id}",
    response_model=Character,
    status_code=status.HTTP_200_OK,
)
def get_character(
    character_id: int,
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> Character:
    """Fetches a specific character from the database

    Args:
        character_id (int): The ID of the character to be fetched
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        NotFoundException: A 404 exception if the character is not found.
        NotAuthorizedException: A 403 exception if the character does not
            belong to the current user

    Returns:
        Character: An dictionary representing the character fetched.
    """

    query = db.query(models.Character).where(
        models.Character.id == character_id
    )

    result = db.execute(query)
    character = result.scalars().first()

    if not character:
        raise NotFoundException(route="character")

    if character.user_id != current_user.id:
        raise NotAuthorizedException(action="get", route="character")

    return character


@router.post(
    "/characters",
    response_model=Character,
    status_code=status.HTTP_201_CREATED,
)
def add_character(
    character: CharacterCreate,
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> Character:
    """Adds the given character to the database

    Args:
        character (CharacterCreate): The character to be added to the database
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        http_err: A caught HTTP error
        HTTPException: A non-HTTP exception caught and raised as an HTTP 500
            exception

    Returns:
        Character: The character added to the database
    """
    try:
        db_character = convert_to_db_character(character, current_user)

        db.add(db_character)
        db.commit()
        db.refresh(db_character)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in add_character: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        )
    return db_character


def convert_to_db_character(
    character: CharacterCreate, user: models.User
) -> models.Character:
    """Reformats a given character to match the model used by the database

    Args:
        character (CharacterCreate): The character being converted
        user (models.User): The user the character should belong to.

    Returns:
        models.Character: A representation of the character ready to be added
            to the database.
    """
    defense_dict = {
        "armor_class": character.defenses.armor_class,
        "saves": {
            "fortitude": character.defenses.saves.fortitude,
            "reflex": character.defenses.saves.reflex,
            "will": character.defenses.saves.will,
        },
    }
    actions_dict = {"attacks": []}
    if character.actions.attacks:
        for attack in character.actions.attacks:
            attack_dict = {
                "name": attack.name,
                "attackBonus": attack.attackBonus,
                "damage": attack.damage,
                "damageType": attack.damageType,
            }
            actions_dict["attacks"].append(attack_dict)

    db_character = models.Character(
        user=user,
        name=character.name,
        player=character.player,
        xp=character.xp,
        ancestry=character.ancestry,
        background=character.background,
        class_=character.class_,
        level=character.level,
        perception=character.perception,
        skills=dict(character.skills),
        attribute_modifiers=dict(character.attribute_modifiers),
        defenses=defense_dict,
        max_hit_points=character.max_hit_points,
        speed=character.speed,
        actions=actions_dict,
    )

    return db_character


@router.patch(
    "/characters", response_model=Character, status_code=status.HTTP_200_OK
)
def update_character(
    character_update: CharacterUpdate,
    db: db_dependency,
    current_user: models.User = Depends(get_current_user),
) -> Character:
    """Updates a given character in the database.

    Uses the ID contained in character_update to fetch a character from the
    database and then uses the rest of character_update to overwrite that
    character's data with the data in character_update.

    Args:
        character_update (CharacterUpdate): A dictionary containing the data to
            be added or changes for the character.
        db (db_dependency): A SQLAlchemy database session
        current_user (models.User, optional): The currently logged in user.
             Defaults to Depends(get_current_user).

    Raises:
        NotFoundException: A 404 exception if the character is not found.
        NotAuthorizedException: A 403 exception if the character does not
            belong to the current user
        http_err: A caught HTTP error
        HTTPException: A non-HTTP exception caught and raised as an HTTP 500
            exception

    Returns:
        Character: The updated character's data
    """
    try:
        db_character = db.get(models.Character, character_update.id)

        if db_character is None:
            raise NotFoundException(route="character")

        if db_character.user_id != current_user.id:
            raise NotAuthorizedException(action="update", route="character")

        update_data = character_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_character, key, value)

        db.commit()
        db.refresh(db_character)

        updated_character = Character.from_orm(db_character)
        return updated_character

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in add_character: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        )


@router.delete(
    "/characters/{character_id}",
    response_model=object,
    status_code=status.HTTP_200_OK,
)
def delete_character(
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
        NotAuthorizedException: A 403 exception if the character does not
            belong to the current user

    Returns:
        object: A response object confirming the character was deleted.
    """
    query = db.query(models.Character).where(
        models.Character.id == character_id
    )

    result = db.execute(query)
    character = result.scalars().first()

    if not character:
        raise NotFoundException(route="character")

    if character.user_id != current_user.id:
        raise NotAuthorizedException(action="delete", route="character")

    db.delete(character)
    db.commit()

    return {"message": "Character deleted"}
