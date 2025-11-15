from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select

import models
from schemas import Character, CharacterCreate, Characters

from ..auth_helpers import get_current_active_user
from ..dependencies import db_dependency

router = APIRouter()
@router.get("/characters", response_model=Characters, status_code=status.HTTP_200_OK)
def get_characters(
    db: db_dependency, current_user: models.User = Depends(get_current_active_user)
):
    query = select(models.Character)
    query = query.where(models.Character.user_id == current_user.id)
    result = db.execute(query)
    characters = result.scalars().all()
    character_list = [e.__dict__ for e in characters]
    return Characters(characters=character_list)

@router.get(
    "/characters/{character_id}",
    response_model=Character,
    status_code=status.HTTP_200_OK,
)
def get_character(character_id, db: db_dependency):
    query = db.query(models.Character).where(models.Character.id == character_id)

    result = db.execute(query)
    character = result.scalars().first()

    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    return character


@router.post(
    "/characters", response_model=Character, status_code=status.HTTP_201_CREATED
)
async def add_character(character: CharacterCreate, db: db_dependency, current_user: models.User = Depends(get_current_active_user)):
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

def convert_to_db_character(character, current_user):
    # Some parts of the dict need to be manually built since the Pydantic models
    # don't covert well to dictionaries when they have models inside models
    defense_dict = {
        "armor_class": character.defenses.armor_class,
        "saves": {
            "fortitude": character.defenses.saves.fortitude,
            "reflex": character.defenses.saves.reflex,
            "will": character.defenses.saves.will,
        },
    }
    actions_dict = {"attacks": []}
    for attack in character.actions.attacks:
        attack_dict = {
            "name": attack.name,
            "attackBonus": attack.attackBonus,
            "damage": attack.damage,
            "damageType": attack.damageType
        }
        actions_dict["attacks"].append(attack_dict)

    db_character = models.Character(
        user=current_user,
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


@router.delete(
    "/characters/{character_id}", response_model=object, status_code=status.HTTP_200_OK
)
def delete_character(
    character_id,
    db: db_dependency,
    current_user: models.User = Depends(get_current_active_user),
):
    query = db.query(models.Character).where(models.Character.id == character_id)

    result = db.execute(query)
    character = result.scalars().first()

    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Character not found"
        )

    if character.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this character",
        )

    db.delete(character)
    db.commit()

    return {"message": "Character deleted"}
