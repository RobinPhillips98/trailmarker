"""Defines helper functions used to import Pathbuilder2e characters."""

import math

from schemas import CharacterCreate, PathbuilderImport


def convert_import_to_character(
    imported_character: PathbuilderImport,
) -> CharacterCreate:
    """Converts a exported Pathbuilder JSON file into a CharacterCreate object

    Args:
        imported_character (PathbuilderImport): An exported JSON file from
            Pathbuilder2e representing a Pathfinder 2E character

    Returns:
        CharacterCreate: The converted character
    """

    attributes_dict = add_attribute_modifiers(imported_character)

    perception = (
        imported_character.proficiencies.perception
        + imported_character.abilities.wis
        + imported_character.level
    )

    skills_dict = add_skills(imported_character, attributes_dict)

    attributes = imported_character.attributes

    defense_dict = {
        "armor_class": imported_character.acTotal.acTotal,
        "saves": {
            "fortitude": (
                imported_character.proficiencies.fortitude
                + imported_character.level
                + attributes_dict["constitution"]
            ),
            "reflex": (
                imported_character.proficiencies.reflex
                + imported_character.level
                + attributes_dict["dexterity"]
            ),
            "will": (
                imported_character.proficiencies.will
                + imported_character.level
                + attributes_dict["wisdom"]
            ),
        },
    }

    attacks = []
    for weapon in imported_character.weapons:
        attacks.append(weapon.name)

    actions_dict = {
        "attacks": attacks,
        "spells": [],
        "heals": 0,
        "shield": int(imported_character.acTotal.shieldBonus),
    }

    proficiencies = {
        "simple": imported_character.proficiencies.simple,
        "martial": imported_character.proficiencies.martial,
    }

    print(proficiencies)

    character = CharacterCreate(
        name=imported_character.name,
        class_=imported_character.class_,
        level=imported_character.level,
        xp=imported_character.xp,
        ancestry=imported_character.ancestry,
        heritage=imported_character.heritage,
        background=imported_character.background,
        perception=perception,
        max_hit_points=(
            attributes.bonushp
            + attributes.bonushp
            + attributes.classhp
            + (imported_character.level * attributes.bonushpPerLevel)
        ),
        speed=attributes.speed,
        attribute_modifiers=attributes_dict,
        skills=skills_dict,
        defenses=defense_dict,
        actions=actions_dict,
        proficiencies=proficiencies,
    )

    return character


def add_attribute_modifiers(
    imported_character: PathbuilderImport,
) -> dict[str, int]:
    """Builds a dictionary of attribute modifiers for the character.

    Args:
        imported_character (PathbuilderImport): An exported JSON file from
            Pathbuilder2e representing a Pathfinder 2E character

    Returns:
        dict[str, int]: A dictionary of attribute modifiers
    """
    abilities = imported_character.abilities
    attributes_dict = {
        "strength": math.floor((abilities.str_ - 10) / 2),
        "dexterity": math.floor((abilities.dex - 10) / 2),
        "constitution": math.floor((abilities.con - 10) / 2),
        "wisdom": math.floor((abilities.wis - 10) / 2),
        "charisma": math.floor((abilities.cha - 10) / 2),
        "intelligence": math.floor((abilities.int_ - 10) / 2),
    }

    return attributes_dict


def add_skills(
    imported_character: PathbuilderImport, attributes_dict: dict[str, int]
) -> dict[str, int]:
    """Builds a dictionary of skill bonuses for the character

    Args:
        imported_character (PathbuilderImport): An exported JSON file from
            Pathbuilder2e representing a Pathfinder 2E character
        attributes_dict (dict[str, int]): The character's already calculated
            attribute modifiers

    Returns:
        dict[str, int]: A dictionary of skill bonuses
    """
    attributes_map = {
        "acrobatics": "dexterity",
        "arcana": "intelligence",
        "athletics": "strength",
        "crafting": "intelligence",
        "deception": "charisma",
        "diplomacy": "charisma",
        "intimidation": "charisma",
        "medicine": "wisdom",
        "nature": "wisdom",
        "occultism": "intelligence",
        "performance": "charisma",
        "religion": "wisdom",
        "society": "intelligence",
        "stealth": "dexterity",
        "survival": "wisdom",
        "thievery": "dexterity",
    }

    skills_dict = {}

    # We want to move past all proficiencies that aren't skills
    start_index = 0
    for proficiency_name in dict(imported_character.proficiencies).keys():
        if proficiency_name == "acrobatics":
            break
        start_index += 1

    for skill_name, profiency_bonus in list(
        dict(imported_character.proficiencies).items()
    )[start_index:]:
        skills_dict[skill_name] = (
            profiency_bonus
            + imported_character.level
            + attributes_dict[attributes_map[skill_name]]
        )

    skills_dict["lore"] = (
        imported_character.lores[0][1]
        + attributes_dict["intelligence"]
        + imported_character.level
    )

    return skills_dict
