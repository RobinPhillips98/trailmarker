"""Defines helper functions related to the characters API route."""

import json
from pathlib import Path

from sqlalchemy.future import select

import models
from schemas import CharacterCreate, Characters


async def fetch_characters_from_db(user, db) -> Characters:
    """Fetches all characters owned by `user`

    Args:
        user: The user whose characters should be fetched
        db: A SQLAlchemy database session

    Returns:
        Characters: A list of Character objects
    """
    query = select(models.Character)
    query = query.where(models.Character.user_id == user.id)
    result = await db.execute(query)
    characters = result.scalars().all()
    character_list = [e.__dict__ for e in characters]
    return Characters(characters=character_list)


def convert_to_db_character(
    character: CharacterCreate, user: models.User
) -> models.Character:
    """Reformats `character` to match the model used by the database

    Args:
        character (CharacterCreate): The character being converted
        user (models.User): The user the character should belong to.

    Returns:
        models.Character: A representation of the character ready to be added
            to the database.
    """
    data_path = "data"
    weapons_path = f"{data_path}/weapons.json"
    weapons_json = json.loads(Path(weapons_path).read_text())
    defense_dict = {
        "armor_class": character.defenses.armor_class,
        "saves": {
            "fortitude": character.defenses.saves.fortitude,
            "reflex": character.defenses.saves.reflex,
            "will": character.defenses.saves.will,
        },
    }
    actions_dict = {
        "attacks": [],
        "spells": [],
        "heals": character.actions.heals,
        "shield": character.actions.shield,
    }
    if character.actions.attacks:
        for attack in character.actions.attacks:
            weapon_json = weapons_json[attack.lower()]

            proficiency_bonus = 0
            type_ = weapon_json["type"].lower()
            name = weapon_json["name"].lower()
            if name in character.extra_proficiencies.keys():
                proficiency_bonus = (
                    character.level + character.extra_proficiencies[name]
                )
            elif type_ in character.proficiencies.keys():
                proficiency_bonus = (
                    character.level + character.proficiencies[type_]
                )

            dex = character.attribute_modifiers.dexterity
            strength = character.attribute_modifiers.strength
            if weapon_json["category"] == "ranged" or (
                "finesse" in weapon_json["traits"] and dex > strength
            ):
                attack_bonus = proficiency_bonus + dex
            else:
                attack_bonus = proficiency_bonus + strength

            damage = weapon_json["damage"]
            if (
                "thief" in character.other_features
                and "finesse" in weapon_json["traits"]
            ):
                damage = f"{damage} + {dex}"
            elif weapon_json["category"] == "melee" and strength > 0:
                damage = f"{damage}+{strength}"

            attack_dict = {
                "name": weapon_json["name"],
                "attackBonus": attack_bonus,
                "damage": damage,
                "damageType": weapon_json["damageType"],
                "range": weapon_json["range"],
                "traits": weapon_json["traits"],
            }
            actions_dict["attacks"].append(attack_dict)

    if character.actions.spells:
        for spell in character.actions.spells:
            spell_dict = {
                "name": spell.name,
                "slots": spell.slots,
                "level": spell.level,
                "damage_roll": spell.damage_roll,
                "damage_type": spell.damage_type,
                "range": spell.range_,
                "area": spell.area,
                "save": spell.save,
                "targets": spell.targets,
                "actions": spell.actions,
            }
            actions_dict["spells"].append(spell_dict)

    db_character = models.Character(
        user=user,
        name=character.name,
        player=character.player,
        xp=character.xp,
        ancestry=character.ancestry,
        heritage=character.heritage,
        background=character.background,
        class_=character.class_,
        level=character.level,
        perception=character.perception,
        skills=dict(character.skills),
        attribute_modifiers=dict(character.attribute_modifiers),
        defenses=defense_dict,
        max_hit_points=character.max_hit_points,
        spell_attack_bonus=character.spell_attack_bonus,
        spell_dc=character.spell_dc,
        speed=character.speed,
        actions=actions_dict,
        proficiencies=character.proficiencies,
        extra_proficiencies=character.extra_proficiencies,
        other_features=character.other_features,
    )

    return db_character
