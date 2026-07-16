"""Defines helper functions related to the characters API route."""

import json
from pathlib import Path
from typing import Any

from sqlalchemy.future import select

import models
from schemas import (
    Character,
    CharacterCreate,
    CreatureCreate,
    CreatureUpdate,
    EnemyCreate,
)


async def fetch_characters_from_db(user, db) -> list[Character]:
    """Fetches all characters owned by `user`

    Args:
        user: The user whose characters should be fetched
        db: A SQLAlchemy database session

    Returns:
        list[Character]: A list of Character objects
    """
    stmt = select(models.Character).where(models.Character.user_id == user.id)
    characters = (await db.scalars(stmt)).all()
    return characters


def _convert_to_db_creature(
    creature: CreatureCreate, user: models.User = None
) -> tuple[CreatureCreate, dict, dict]:
    """Reformats `creature` to match the model used by the database.

    Args:
        creature (CreatureCreate): The creature being converted
        user (models.User, optional): The user the creature should belong to.
            Defaults to None.

    Returns:
        tuple[CreatureCreate, dict, dict]: A tuple containing the creature,
            its actions dictionary, and its defense dictionary.
    """
    data_path = "data"
    weapons_path = f"{data_path}/weapons.json"
    weapons_json = json.loads(Path(weapons_path).read_text())
    spells_path = f"{data_path}/spells.json"
    spells_json = json.loads(Path(spells_path).read_text())

    defense_dict = {
        "armor_class": creature.defenses.armor_class,
        "saves": {
            "fortitude": creature.defenses.saves.fortitude,
            "reflex": creature.defenses.saves.reflex,
            "will": creature.defenses.saves.will,
        },
    }

    attack_list = []
    spell_list = []

    if creature.actions.attacks:
        attack_list = build_attack_list(creature, weapons_json)
    if creature.actions.spells:
        spell_list = build_spell_list(creature, spells_json)

    actions_dict = {
        "attacks": attack_list,
        "spells": spell_list,
        "heals": creature.actions.heals,
        "shield": creature.actions.shield,
        "sneak_attack": creature.actions.sneak_attack,
    }

    return creature, actions_dict, defense_dict


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
    creature, actions_dict, defense_dict = _convert_to_db_creature(
        character, user
    )

    return models.Character(
        user=user,
        name=creature.name,
        player=creature.player,
        xp=creature.xp,
        ancestry=creature.ancestry,
        heritage=creature.heritage,
        background=creature.background,
        class_=creature.class_,
        level=creature.level,
        perception=creature.perception,
        skills=dict(creature.skills),
        attribute_modifiers=dict(creature.attribute_modifiers),
        defenses=defense_dict,
        max_hit_points=creature.max_hit_points,
        spell_attack_bonus=creature.spell_attack_bonus,
        spell_dc=creature.spell_dc,
        speed=creature.speed,
        actions=actions_dict,
        proficiencies=creature.proficiencies,
        extra_proficiencies=creature.extra_proficiencies,
        other_features=creature.other_features,
    )


def convert_to_db_enemy(enemy):
    """Reformats `enemy` to match the model used by the database

    Args:
        enemy (EnemyCreate): The enemy being converted

    Returns:
        models.Enemy: A representation of the enemy ready to be added
            to the database.
    """
    creature, actions_dict, defense_dict = _convert_to_db_creature(enemy)

    return models.Enemy(
        name=creature.name,
        level=creature.level,
        perception=creature.perception,
        skills=dict(creature.skills),
        attribute_modifiers=dict(creature.attribute_modifiers),
        defenses=defense_dict,
        max_hit_points=creature.max_hit_points,
        spell_attack_bonus=creature.spell_attack_bonus,
        spell_dc=creature.spell_dc,
        speed=creature.speed,
        actions=actions_dict,
        traits=creature.traits,
        immunities=creature.immunities,
        weaknesses=creature.weaknesses,
        resistances=creature.resistances,
    )


def build_attack_list(
    creature: CreatureCreate | CreatureUpdate,
    weapons_json: dict[str, Any] = None,
) -> list[dict[str, Any]]:
    """Uses weapon names to build a list of attack objects from saved data.

    Args:
        creature (CreatureCreate | CreatureUpdate): The creature whose
            attacks are being built
        weapons_json (dict[str, Any], optional): The dictionary containing the
            data with stats for each weapon. Defaults to None.

    Returns:
        list[dict[str, Any]]: A list of attack objects built from weapon data,
            ready to be stored in the database
    """
    if not weapons_json:
        data_path = "data"
        weapons_path = f"{data_path}/weapons.json"
        weapons_json = json.loads(Path(weapons_path).read_text())

    attack_list = []

    for attack in creature.actions.attacks:
        weapon_json = weapons_json[attack.lower()]

        proficiency_bonus = 0
        type_ = weapon_json["type"].lower()
        name = weapon_json["name"].lower()
        if name in creature.extra_proficiencies.keys():
            proficiency_bonus = (
                max(creature.level, 1) + creature.extra_proficiencies[name]
            )
        elif type_ in creature.proficiencies.keys():
            proficiency_bonus = (
                max(creature.level, 1) + creature.proficiencies[type_]
            )

        dex = creature.attribute_modifiers.dexterity
        strength = creature.attribute_modifiers.strength
        if weapon_json["category"] == "ranged" or (
            "finesse" in weapon_json["traits"] and dex > strength
        ):
            attack_bonus = proficiency_bonus + dex
        else:
            attack_bonus = proficiency_bonus + strength

        damage = weapon_json["damage"]
        if (
            (
                isinstance(creature, CharacterCreate)
                and "thief" in creature.other_features
            )
            or (isinstance(creature, EnemyCreate) and creature.use_finesse)
            and "finesse" in weapon_json["traits"]
        ):
            damage = f"{damage}+{dex}"
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
        attack_list.append(attack_dict)
    return attack_list


def build_spell_list(
    creature: CreatureCreate | CreatureUpdate,
    spells_json: dict[str, Any] = None,
) -> list[dict[str, Any]]:
    """Uses spell names to build a list of spell objects from saved data.

    Args:
        creature (CreatureCreate | CreatureUpdate): The creature whose
            spells are being built
        spells_json (dict[str, Any], optional): The dictionary containing
         the data with stats for each spell. Defaults to None.

    Returns:
        list[dict[str, Any]]: A list of spell objects built from spell data,
            ready to be stored in the database
    """
    if not spells_json:
        data_path = "data"
        spells_path = f"{data_path}/spells.json"
        spells_json = json.loads(Path(spells_path).read_text())

    spell_list = []

    for spell in creature.actions.spells.keys():
        spell_json = spells_json[spell.lower()]
        spell_dict = spell_json.copy()
        spell_dict["slots"] = creature.actions.spells[spell]
        spell_list.append(spell_dict)

    return spell_list
