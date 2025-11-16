import json
import os
import shutil
import sys
from pathlib import Path

import requests
from github import Github


def fetch_data(raw_path: str, bestiary_path: str, rebuild: bool) -> None:
    """Fetches each of the files from GitHub and stores them in the raw_data folder"""  # noqa
    check_dir(raw_path)

    base_url = "https://raw.githubusercontent.com/foundryvtt/pf2e/refs/heads/v13-dev/packs/menace-under-otari-bestiary/"  # noqa
    # Getting the files with PyGithub directly takes too long and results in
    # being rate-limited, so just get the filenames with it
    filenames = get_filenames()

    print("Downloading raw files...")
    for filename in filenames:
        if check_skip(rebuild, bestiary_path, filename):
            continue

        path = Path(f"{raw_path}{filename}")
        url = f"{base_url}{filename}"

        print(f"Requesting {filename}...")
        r = requests.get(url)
        print(f"Writing {filename}...")
        path.write_text(r.text)
        print(f"{filename} saved\n")

    print("Raw files downloaded\n")


def convert_data(raw_path: str, bestiary_path: str, rebuild: bool) -> None:
    """Convert each file in raw_data to a format that works better for Trailmarker"""  # noqa
    errors_found = False
    error_list = []

    check_dir(bestiary_path)

    files = os.listdir(raw_path)
    files.sort()
    for file in files:
        if check_skip(rebuild, bestiary_path, file):
            continue

        path = Path(f"{raw_path}{file}")
        print(f"Loading {file}...")
        try:
            raw_dict = json.loads(path.read_text())
        except json.decoder.JSONDecodeError:
            print(f"ERROR: could not decode {file}.")
            errors_found = True
            error_list.append(file)
            continue

        print(f"Reformatting {file}...")
        enemy = build_enemy_dict(raw_dict)

        reformatted_file = file.replace("-bb", "")
        print(f"Saving {reformatted_file}...\n")
        path = Path(f"{bestiary_path}{reformatted_file}")
        enemy_json = json.dumps(enemy, indent=4)
        path.write_text(enemy_json)

    if errors_found:
        print("NOTE: The following files had errors:")
        for file in error_list:
            print(f"\t{file}")

    print("Files reformatted.\n")


def check_dir(dir: str) -> None:
    """Creates needed directory if it doesn't exist"""
    if not (Path(dir).exists()):
        Path(dir).mkdir()


def get_filenames() -> list[str]:
    """Uses PyGithub to return a list of filenames retrieved from GitHub"""
    g = Github()
    repo = g.get_repo("foundryvtt/pf2e")
    files = repo.get_contents("packs/menace-under-otari-bestiary")
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


def check_skip(rebuild: bool, bestiary_path: str, filename: str) -> bool:
    if rebuild:
        return False

    reformatted_file = filename.replace("-bb", "")
    if Path(f"{bestiary_path}{reformatted_file}").exists():
        print(f"{reformatted_file} already exists, skipping {filename}\n")
        return True
    else:
        return False


def build_enemy_dict(raw_dict: dict[any]) -> dict[any]:
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
            "armorClass": 0,
            "saves": {"fortitude": 0, "reflex": 0, "will": 0},
        },
        "max_hit_points": 0,
        "immunities": [],
        "speed": 0,
        "actions": {"attacks": []},
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

    enemy["speed"] = system_attributes["speed"]["value"]

    add_attacks(raw_dict, enemy)

    return enemy


def add_traits(raw_dict: dict[any], enemy: dict[any]) -> None:
    enemy["traits"].append(raw_dict["system"]["traits"]["rarity"])
    enemy["traits"].append(raw_dict["system"]["traits"]["size"]["value"])

    traits = raw_dict["system"]["traits"]["value"]
    for trait in traits:
        enemy["traits"].append(trait)


def add_skills(raw_dict: dict[any], enemy: dict[any]) -> None:
    skills = raw_dict["system"]["skills"]
    for skill in skills:
        enemy["skills"][skill] = skills[skill]["base"]


def add_attribute_modifiers(raw_dict: dict[any], enemy: dict[any]) -> None:
    abilities = raw_dict["system"]["abilities"]
    enemy["attribute_modifiers"]["strength"] = abilities["str"]["mod"]
    enemy["attribute_modifiers"]["dexterity"] = abilities["dex"]["mod"]
    enemy["attribute_modifiers"]["constitution"] = abilities["con"]["mod"]
    enemy["attribute_modifiers"]["intelligence"] = abilities["int"]["mod"]
    enemy["attribute_modifiers"]["wisdom"] = abilities["wis"]["mod"]
    enemy["attribute_modifiers"]["charisma"] = abilities["cha"]["mod"]


def add_saves(raw_dict: dict[any], enemy: dict[any]) -> None:
    saves = raw_dict["system"]["saves"]
    for save in saves:
        enemy["defenses"]["saves"][save] = saves[save]["value"]


def add_immunities(system_attributes: dict[any], enemy: dict[any]):
    immunities = system_attributes["immunities"]
    for immunity in immunities:
        enemy["immunities"].append(immunity["type"])


def add_attacks(raw_dict, enemy):
    items = raw_dict["items"]
    for item in items:
        if "attack" in item["system"]:
            attack_dict = {}
            attack_dict["name"] = item["name"]
            attack_dict["attackBonus"] = item["system"]["bonus"]["value"]
            # for some reason in the JSON files from foundryVTT there is a
            # key with a random value between damageRolls and the values
            # inside it that I need, thus the damage_roll_key variable
            try:
                damage_rolls = item["system"]["damageRolls"]
                key = list(damage_rolls.keys())[0]
                attack_dict["damage"] = damage_rolls[key]["damage"]
                attack_dict["damageType"] = damage_rolls[key]["damageType"]
            except IndexError:
                pass  # Some attacks don't do damage, so don't add them
            enemy["actions"]["attacks"].append(attack_dict)


def usage_error() -> None:
    usage = f"""Usage: python {sys.argv[0]} [options]
            --rebuild\t rebuild data from scratch"""
    print(usage)
    exit()


def main():
    parent_directory = str(Path(__file__).parent.parent)
    raw_path = f"{parent_directory}/raw_data/"
    bestiary_path = f"{parent_directory}/bestiary/"

    rebuild = False

    if len(sys.argv) == 2:
        if sys.argv[1] == "--rebuild":
            rebuild = True
            if Path(f"{raw_path}").exists():
                shutil.rmtree(raw_path)
            if Path(f"{bestiary_path}").exists():
                shutil.rmtree(bestiary_path)
        else:
            usage_error()
    elif len(sys.argv) > 2:
        usage_error()

    fetch_data(raw_path, bestiary_path, rebuild)
    convert_data(raw_path, bestiary_path, rebuild)

    print("Cleaning up...")
    shutil.rmtree(raw_path)

    print("Initialization complete!")


if __name__ == "__main__":
    main()
