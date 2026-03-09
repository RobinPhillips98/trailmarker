"""Defines helper functions used to import Pathbuilder2e characters."""

import json
import math
from collections import defaultdict
from pathlib import Path

from schemas import (
    CharacterCreate,
    PathbuilderImport,
    PathbuilderSpecificProficiencies,
)


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
        + attributes_dict["wisdom"]
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
    data_path = "data"
    weapons_path = f"{data_path}/weapons.json"
    weapons_json = json.loads(Path(weapons_path).read_text())
    valid_weapons = [value.get("name") for value in weapons_json.values()]
    for weapon in imported_character.weapons:
        if weapon.name in valid_weapons:
            attacks.append(weapon.name)

    spells = {}
    num_heals = 0
    spell_bonuses = {
        "spell_attack_bonus": 0,
        "spell_dc": 0,
    }
    if imported_character.spellCasters:
        spells, num_heals = add_spells(
            imported_character, spell_bonuses, attributes_dict
        )

    actions_dict = {
        "attacks": attacks,
        "spells": spells,
        "heals": num_heals,
        "shield": (
            int(imported_character.acTotal.shieldBonus)
            if imported_character.acTotal.shieldBonus
            else 0
        ),
    }

    proficiencies = {
        "simple": imported_character.proficiencies.simple,
        "martial": imported_character.proficiencies.martial,
    }

    extra_proficiencies = add_extra_proficiencies(
        imported_character.specificProficiencies
    )

    other_features = check_for_other_features(imported_character)

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
            attributes.ancestryhp
            + attributes.bonushp
            + (imported_character.level * attributes.classhp)
            + (imported_character.level * attributes_dict["constitution"])
            + (imported_character.level * attributes.bonushpPerLevel)
        ),
        spell_attack_bonus=spell_bonuses["spell_attack_bonus"],
        spell_dc=spell_bonuses["spell_dc"],
        speed=attributes.speed,
        attribute_modifiers=attributes_dict,
        skills=skills_dict,
        defenses=defense_dict,
        actions=actions_dict,
        proficiencies=proficiencies,
        extra_proficiencies=extra_proficiencies,
        other_features=other_features,
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

    for skill_name, proficiency_bonus in list(
        dict(imported_character.proficiencies).items()
    )[start_index:]:
        if proficiency_bonus > 0:
            proficiency_bonus += imported_character.level
        skills_dict[skill_name] = (
            proficiency_bonus + attributes_dict[attributes_map[skill_name]]
        )

    skills_dict["lore"] = (
        imported_character.lores[0][1]
        + attributes_dict["intelligence"]
        + imported_character.level
    )

    return skills_dict


def add_spells(
    imported_character: PathbuilderImport,
    spell_bonuses: dict[str, int],
    attributes_dict: dict[str, int],
):
    spellcaster = imported_character.spellCasters[0]

    calculate_spell_bonuses(
        spellcaster, imported_character, attributes_dict, spell_bonuses
    )

    spells = defaultdict(int)

    num_heals = 0

    data_path = "data"
    spells_path = f"{data_path}/spells.json"
    spells_json = json.loads(Path(spells_path).read_text())
    valid_spells = [value.get("name") for value in spells_json.values()]

    spell_lists = spellcaster.prepared or spellcaster.spells

    for spell_list in spell_lists:
        for spell in spell_list["list"]:
            if spell in valid_spells:
                spell_name = spell.lower().replace(" ", "_")
                spells[spell_name] += 1
            elif spell.lower() == "heal":
                num_heals += 1

    for spellcaster_dict in imported_character.spellCasters:
        if spellcaster_dict.name == "Cleric Font":
            for spell_list in spellcaster_dict.spells:
                for spell in spell_list["list"]:
                    if spell.lower() == "heal":
                        num_heals += 1

    """I know it looks like this is incredibly unoptimized, but in the vast
    majority of use cases, particularly in the Beginner Box version, both the
    first and second loop will actually only have one iteration,
    "for spell in focus_dict["focusCantrips"]:" will probably not have any
    iterations, and "for spell in focus_dict["focusSpells"]:" will likely only
    have a few iterations at most. I thought about just doing keys()[0] for
    the first two, but made them loops just in case there is actually more than
    one object within focus. For reference, focus will typically look something
    like this:
    "focus": {
      "arcane": {
        "int": {
          "abilityBonus": 4,
          "proficiency": 2,
          "itemBonus": 0,
          "focusCantrips": [],
          "focusSpells": ["Force Bolt"]
        }
      }
    }
    Runtime complexity: O(x * y * (c + s)) where
    x = the number of outer dictionaries,
    y = the number of inner dictionaries,
    c = the number of cantrips and
    s = the number of spells.
    However, typically: x = 1, y = 1, c = 0, and s <= 3, so effectively this is
    1 * 1 * (0 + 3) <= 3 iterations
    """
    if imported_character.focus:
        for key_1 in list(imported_character.focus.keys()):
            for key_2 in list(imported_character.focus[key_1].keys()):
                focus_dict = imported_character.focus[key_1][key_2]
                for cantrip in focus_dict["focusCantrips"]:
                    if cantrip in valid_spells:
                        cantrip_name = cantrip.lower().replace(" ", "_")
                        spells[cantrip_name] += 1
                for spell in focus_dict["focusSpells"]:
                    if spell in valid_spells:
                        spell_name = spell.lower().replace(" ", "_")
                        spells[spell_name] += 1

    return [spells, num_heals]


def calculate_spell_bonuses(
    spellcaster, imported_character, attributes_dict, spell_bonuses
):
    spell_attack_bonus = spellcaster.proficiency + imported_character.level

    match spellcaster.ability:
        case "int":
            spell_attack_bonus += attributes_dict["intelligence"]
        case "wis":
            spell_attack_bonus += attributes_dict["wisdom"]
        case "cha":
            spell_attack_bonus += attributes_dict["charisma"]
        case _:
            raise ValueError("Invalid spellcasting ability")

    spell_bonuses["spell_attack_bonus"] = spell_attack_bonus
    spell_bonuses["spell_dc"] = spell_attack_bonus + 10


def add_extra_proficiencies(proficiencies: PathbuilderSpecificProficiencies):
    extra_proficiencies = {}

    for proficiency in proficiencies.trained:
        name = proficiency.lower().replace(" ", "_")
        extra_proficiencies[name] = 2

    for proficiency in proficiencies.expert:
        name = proficiency.lower().replace(" ", "_")
        extra_proficiencies[name] = 4

    return extra_proficiencies


def check_for_other_features(
    imported_character: PathbuilderImport,
) -> list[str]:
    other_features = []
    features_set = set()
    valid_features = {"Thief Racket"}
    feature_conversions = {"Thief Racket": "thief"}

    for feat_list in imported_character.feats:
        if not valid_features.isdisjoint(feat_list):
            features_set.update(valid_features.intersection(feat_list))

    if not valid_features.isdisjoint(imported_character.specials):
        features_set.update(
            valid_features.intersection(imported_character.specials)
        )

    if features_set:
        other_features = list(features_set)
        other_features = [
            feature_conversions[feature] for feature in other_features
        ]

    return other_features
