import argparse
import json
import os
import shutil
from pathlib import Path

import requests
from github import Github
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import engine_sync
from models import Base, Enemy


def initialize_enemies(db: Session):
    """Initializes the enemies table in the database.

    Fetches the files for the enemies from GitHub, converts them to a format
    that suits the database, and then adds them to the database.

    Args:
        db (Session): A SQLAlchemy database session
    """
    raw_path = "raw_data/"

    fetch_enemies(raw_path)
    add_enemies(raw_path, db)

    print("Cleaning up...")
    shutil.rmtree(raw_path)

    print("Initialization complete!")


def fetch_enemies(raw_path: str) -> None:
    """Fetches the enemy files from GitHub and saves them.

    Args:
        raw_path (str): The path of the directory in which the raw data files
        should be saved.
    """
    if not (Path(raw_path).exists()):
        Path(raw_path).mkdir()

    base_url = "https://raw.githubusercontent.com/foundryvtt/pf2e/refs/heads/v13-dev/packs/pf2e/menace-under-otari-bestiary/"  # noqa
    # Getting the files with PyGithub directly takes too long and results in
    # being rate-limited, so just get the filenames with it
    filenames = get_filenames()

    print("Downloading raw files...")
    for filename in filenames:
        path = Path(f"{raw_path}{filename}")
        url = f"{base_url}{filename}"

        print(f"Requesting {filename}...")
        r = requests.get(url)
        print(f"Writing {filename}...")
        path.write_text(r.text)
        print(f"{filename} saved\n")

    print("Raw files downloaded\n")


def get_filenames() -> list[str]:
    repo = Github().get_repo("foundryvtt/pf2e")
    files = repo.get_contents("packs/pf2e/menace-under-otari-bestiary")
    exclusions = [
        "central-spears-bb.json",
        "envenomed-lock-bb.json",
        "falling-ceiling-bb.json",
        "hidden-pit-bb.json",
        "mermaid-fountain-bb.json",
        "scythe-blades-bb.json",
        "slamming-door-bb.json",
        "spear-launcher-bb.json",
        "kobold-boss-zolgran-bb.json",
    ]
    return [file.name for file in files if not (file.name in exclusions)]


def add_enemies(raw_path: str, db: Session) -> None:
    """Iterates through the saved enemies and adds them all to the database

    Args:
        raw_path (str): The path where the enemy files are saved
        db (Session): A SQLAlchemy database session
    """
    errors_found = False
    error_list = []

    files = os.listdir(raw_path)
    files.sort()
    for file in files:

        path = Path(f"{raw_path}{file}")
        print(f"Loading {file}...")
        try:
            raw_dict = json.loads(path.read_text())
        except json.decoder.JSONDecodeError:
            print(f"ERROR: could not decode {file}.")
            errors_found = True
            error_list.append(file)
            continue

        print(f"Building enemy from {file}...")
        enemy = build_enemy_dict(raw_dict)

        try:
            db_enemy = convert_to_db_enemy(enemy)
            print(f"Adding {db_enemy.name} to database...")

            db.add(db_enemy)
            db.commit()
            db.refresh(db_enemy)
        except Exception as e:
            print(f"Error in add_enemies: {str(e)}")
            print(f"Enemy: {enemy}")
            errors_found = True
            error_list.append(file)
            continue

    if errors_found:
        print("NOTE: The following files had errors:")
        for file in error_list:
            print(f"\t{file}")
    else:
        print("No errors occured while adding enemies.")

    print("Enemies added to database!")


def build_enemy_dict(raw_dict: dict[str, any]) -> dict[str, any]:
    """Converts the json file into a reformatted dictionary

    Args:
        raw_dict (dict[str, any]): The raw data retrieved from GitHub

    Returns:
        dict[str, any]: The reformatted data
    """
    enemy = {
        "name": "",
        "level": 0,
        "traits": [],
        "perception": 0,
        "skills": {},
        "attribute_modifiers": {
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0,
        },
        "defenses": {
            "armor_class": 0,
            "saves": {"fortitude": 0, "reflex": 0, "will": 0},
        },
        "max_hit_points": 0,
        "spell_dc": None,
        "spell_attack_bonus": None,
        "immunities": [],
        "weaknesses": {},
        "resistances": {},
        "speed": 0,
        "actions": {"attacks": [], "spells": []},
    }

    enemy["name"] = raw_dict["prototypeToken"]["name"]
    enemy["level"] = raw_dict["system"]["details"]["level"]["value"]

    add_traits(raw_dict, enemy)

    enemy["perception"] = raw_dict["system"]["perception"]["mod"]

    add_skills(raw_dict, enemy)

    add_attribute_modifiers(raw_dict, enemy)

    system_attributes = raw_dict["system"]["attributes"]
    enemy["defenses"]["armor_class"] = system_attributes["ac"]["value"]
    add_saves(raw_dict, enemy)

    enemy["max_hit_points"] = system_attributes["hp"]["max"]
    if "immunities" in system_attributes:
        add_immunities(system_attributes, enemy)

    if "weaknesses" in system_attributes:
        add_weaknesses(system_attributes, enemy)

    if "resistances" in system_attributes:
        add_resistances(system_attributes, enemy)

    enemy["speed"] = system_attributes["speed"]["value"]

    add_actions(raw_dict, enemy)

    return enemy


def add_traits(raw_dict: dict[str, any], enemy: dict[str, any]) -> None:
    size = raw_dict["system"]["traits"]["size"]["value"]
    match size:
        case "tiny":
            enemy["traits"].append("tiny")
        case "sm":
            enemy["traits"].append("small")
        case "med":
            enemy["traits"].append("medium")
        case "lg":
            enemy["traits"].append("large")
        case _:
            raise Exception(f"Invalid size trait: {size}")
    # enemy["traits"].append(raw_dict["system"]["traits"]["size"]["value"])

    traits = raw_dict["system"]["traits"]["value"]
    trait_exceptions = ["chaotic", "lawful", "good", "evil"]
    for trait in traits:
        if trait in trait_exceptions:
            continue
        else:
            enemy["traits"].append(trait)


def add_skills(raw_dict: dict[str, any], enemy: dict[str, any]) -> None:
    skills = raw_dict["system"]["skills"]
    for skill in skills:
        enemy["skills"][skill] = skills[skill]["base"]


def add_attribute_modifiers(
    raw_dict: dict[str, any], enemy: dict[str, any]
) -> None:
    abilities = raw_dict["system"]["abilities"]
    enemy["attribute_modifiers"]["strength"] = abilities["str"]["mod"]
    enemy["attribute_modifiers"]["dexterity"] = abilities["dex"]["mod"]
    enemy["attribute_modifiers"]["constitution"] = abilities["con"]["mod"]
    enemy["attribute_modifiers"]["intelligence"] = abilities["int"]["mod"]
    enemy["attribute_modifiers"]["wisdom"] = abilities["wis"]["mod"]
    enemy["attribute_modifiers"]["charisma"] = abilities["cha"]["mod"]


def add_saves(raw_dict: dict[str, any], enemy: dict[str, any]) -> None:
    saves = raw_dict["system"]["saves"]
    for save in saves:
        enemy["defenses"]["saves"][save] = saves[save]["value"]


def add_immunities(
    system_attributes: dict[str, any], enemy: dict[str, any]
) -> None:
    immunities = system_attributes["immunities"]
    for immunity in immunities:
        enemy["immunities"].append(immunity["type"])


def add_weaknesses(
    system_attributes: dict[str, any], enemy: dict[str, any]
) -> None:
    weaknesses = system_attributes["weaknesses"]
    for weakness in weaknesses:
        enemy["weaknesses"][weakness["type"]] = weakness["value"]


def add_resistances(
    system_attributes: dict[str, any], enemy: dict[str, any]
) -> None:
    resistances = system_attributes["resistances"]
    for resistance in resistances:
        enemy["resistances"][resistance["type"]] = resistance["value"]


def add_actions(raw_dict: dict[str, any], enemy: dict[str, any]) -> None:
    items = raw_dict["items"]
    for item in items:
        if "attack" in item["system"]:
            add_attack(item, enemy)
        elif item["type"] == "spellcastingEntry" and enemy["spell_dc"] is None:
            enemy["spell_dc"] = item["system"]["spelldc"]["dc"]
            enemy["spell_attack_bonus"] = item["system"]["spelldc"]["value"]
        elif item["type"] == "spell" and item["system"]["damage"]:
            add_spell(item, enemy)


def add_attack(item: dict[str, any], enemy: dict[str, any]) -> None:
    attack_dict = {}
    attack_dict["name"] = item["name"]
    attack_dict["attackBonus"] = item["system"]["bonus"]["value"]
    # for some reason in the JSON files from foundryVTT there is a
    # key with a random value between damageRolls and the values
    # inside it that I need, thus the key variable
    try:
        damage_rolls = item["system"]["damageRolls"]
        key = list(damage_rolls.keys())[0]
        attack_dict["damage"] = damage_rolls[key]["damage"]
        attack_dict["damageType"] = damage_rolls[key]["damageType"]
    except IndexError:
        pass  # Some attacks don't do damage, so don't add them
    if item["system"]["range"]:
        attack_dict["range"] = item["system"]["range"]["increment"]
    enemy["actions"]["attacks"].append(attack_dict)


def add_spell(item: dict[str, any], enemy: dict[str, any]) -> None:
    spell_dict = {}
    raw_spell_dict = item["system"]
    spell_dict["name"] = item["name"]

    for spell in enemy["actions"]["spells"]:
        if spell["name"] == spell_dict["name"]:
            spell["slots"] += 1
            return

    spell_dict["slots"] = 1
    spell_dict["level"] = raw_spell_dict["level"]["value"]
    if "cantrip" in raw_spell_dict["traits"]["value"]:
        spell_dict["level"] = 0

    spell_dict["damage_roll"] = raw_spell_dict["damage"]["0"]["formula"]
    spell_dict["damage_type"] = raw_spell_dict["damage"]["0"]["type"]
    spell_dict["range"] = raw_spell_dict["range"]["value"]
    spell_dict["area"] = raw_spell_dict["area"]
    spell_dict["target"] = raw_spell_dict["target"]["value"]

    try:
        if "save" in raw_spell_dict["defense"]:
            spell_dict["save"] = raw_spell_dict["defense"]["save"]["statistic"]
    except TypeError:
        pass  # No save, don't need to add it if it doesn't exist

    spell_dict["actions"] = raw_spell_dict["time"]["value"]

    enemy["actions"]["spells"].append(spell_dict)


def convert_to_db_enemy(enemy: dict[str, any]) -> Enemy:
    """Reformats a given enemy to match the model used by the database

    Args:
        enemy (EnemyCreate): The enemy being converted

    Returns:
        models.Enemy: A representation of the enemy ready to be added to
            the database.
    """
    defense_dict = {
        "armor_class": enemy["defenses"]["armor_class"],
        "saves": {
            "fortitude": enemy["defenses"]["saves"]["fortitude"],
            "reflex": enemy["defenses"]["saves"]["reflex"],
            "will": enemy["defenses"]["saves"]["will"],
        },
    }
    actions_dict = {"attacks": [], "spells": []}
    for attack in enemy["actions"]["attacks"]:
        attack_dict = {
            "name": attack["name"],
            "attackBonus": attack["attackBonus"],
        }
        try:
            attack_dict["damage"] = attack["damage"]
            attack_dict["damageType"] = attack["damageType"]
        except KeyError:
            pass
        try:
            attack_dict["range"] = attack["range"]
        except KeyError:
            pass
        actions_dict["attacks"].append(attack_dict)

    for spell in enemy["actions"]["spells"]:
        actions_dict["spells"].append(spell)

    db_enemy = Enemy(
        name=enemy["name"],
        level=enemy["level"],
        traits=enemy["traits"],
        perception=enemy["perception"],
        skills=enemy["skills"],
        attribute_modifiers=enemy["attribute_modifiers"],
        defenses=defense_dict,
        max_hit_points=enemy["max_hit_points"],
        spell_dc=enemy["spell_dc"],
        spell_attack_bonus=enemy["spell_attack_bonus"],
        immunities=enemy["immunities"],
        weaknesses=enemy["weaknesses"],
        resistances=enemy["resistances"],
        speed=enemy["speed"],
        actions=actions_dict,
    )

    return db_enemy


def drop_all_tables(engine=engine_sync):
    """Drop all tables in the database"""
    print("Starting table operations...")
    try:
        # Drop all tables
        print("Dropping all tables...")
        Base.metadata.drop_all(engine)
        # Clear any remaining connections
        print("Disposing engine...")
        engine.dispose()
        # Recreate empty tables
        print("Creating tables...")
        Base.metadata.create_all(engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error in drop_all_tables: {str(e)}")
        raise


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rebuild", action="store_true", help="Rebuild the database"
    )
    args = parser.parse_args()

    # Print database URL (with password masked)
    db_url = str(engine_sync.url)
    print(f"Database URL: {db_url}")
    if "postgresql" in db_url:
        print(f"Connecting to database: {db_url.split('@')[1]}")

    if args.rebuild:
        print(
            """
###############################################
# Database Rebuild                            #
###############################################
--rebuild flag detected.
Dropping all tables and recreating the database
from scratch.
###############################################
            """
        )
        try:
            print("Dropping all tables...")
            drop_all_tables()
            print("Tables dropped successfully")
        except Exception as e:
            print(f"Error dropping tables: {e}")
            raise

    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine_sync)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise

    with Session(bind=engine_sync) as db:
        try:
            # Check if we already have data
            if (
                args.rebuild
                or db.execute(select(Enemy).limit(1)).first() is None
            ):
                print("Populating enemy data...")
                initialize_enemies(db)
            else:
                print("Enemies already exist, skipping enemy creation")

        except Exception as e:
            print(f"Error populating database: {e}")
            raise  # This will show the full stack trace


if __name__ == "__main__":
    main()
