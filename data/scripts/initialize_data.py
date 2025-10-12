from pathlib import Path
import json, os, requests, shutil, sys

def fetch_data(parent_directory: str, raw_path: str, bestiary_path: str, rebuild: bool) -> None:
    """ Fetches each of the files from GitHub and stores them in the raw_data folder."""

    # TODO: Find way to fetch files from folder on github automatically
    base_url = "https://raw.githubusercontent.com/foundryvtt/pf2e/refs/heads/v13-dev/packs/menace-under-otari-bestiary/"
    filenames = [
        "animated-armor-bb.json",
        "basilisk-bb.json",
        "boar-bb.json",
        "brine-shark-bb.json",
        "bugbear-prowler-bb.json",
        "caligni-dancer-bb.json",
        "caligni-hunter-bb.json",
        "caligni-skulker-bb.json",
        "cinder-rat-bb.json",
        "doppelganger-bb.json",
        "drow-priestess-bb.json",
        "drow-sneak-bb.json",
        "drow-warrior-bb.json",
        "forest-troll-bb.json",
        "gargoyle-bb.json",
        "ghost-commoner-bb.json",
        "ghoul-stalker-bb.json",
        "giant-ant-bb.json",
        "giant-centipede-bb.json",
        "giant-rat-bb.json",
        "giant-spider-bb.json",
        "giant-viper-bb.json",
        "goblin-commando-bb.json",
        "goblin-igniter-bb.json",
        "goblin-warrior-bb.json",
        "harpy-bb.json",
        "hell-hound-bb.json",
        "hobgoblin-soldier-bb.json",
        "horned-dragon-juvenile-bb.json",
        "kobold-boss-zolgran-bb.json",
        "kobold-dragon-mage-black-bb.json",
        "kobold-dragon-mage-blue-bb.json",
        "kobold-dragon-mage-green-bb.json",
        "kobold-dragon-mage-red-bb.json",
        "kobold-scout-bb.json",
        "kobold-trapmaster-bb.json",
        "kobold-warrior-bb.json",
        "leopard-bb.json",
        "mimic-bb.json",
        "minotaur-hunter-bb.json",
        "ogre-warrior-bb.json",
        "orc-commander-bb.json",
        "orc-scrapper-bb.json",
        "orc-veteran-bb.json",
        "owlbear-bb.json",
        "pugwampi-bb.json",
        "reefclaw-bb.json",
        "sewer-ooze-bb.json",
        "shadow-bb.json",
        "skeletal-giant-bb.json",
        "skeleton-guard-bb.json",
        "sod-hound-bb.json",
        "viper-bb.json",
        "warg-bb.json",
        "web-lurker-bb.json",
        "wight-bb.json",
        "wolf-bb.json",
        "xulgath-leader-bb.json",
        "xulgath-warrior-bb.json",
        "zephyr-hawk-bb.json",
        "zombie-shambler-bb.json"
    ]
    if not (Path(raw_path).exists()):
        Path(raw_path).mkdir()

    print("Downloading raw files...")
    for filename in filenames:
        save_path = f"{raw_path}{filename}"
        path = Path(save_path)
        if not rebuild:
            reformatted_file = filename.replace("-bb", "")
            if Path(f"{bestiary_path}{reformatted_file}").exists():
                print(f"{reformatted_file} already exists, skipping {filename} \n")
                continue

            if path.exists():
                print(f"{filename} already exists, skipping {filename} \n")
                continue
            
        url = f"{base_url}{filename}"
        print(f"Requesting {filename}...")
        r = requests.get(url)
        print(f"Writing {filename}...")
        path.write_text(r.text)
        print(f"{filename} saved\n")

    print("Raw files downloaded\n")

def convert_data(parent_directory: str, raw_path: str, bestiary_path: str, rebuild: bool) -> None:
    if not (Path(bestiary_path).exists()):
        Path(bestiary_path).mkdir()
    
    files = os.listdir(raw_path)
    for file in files:
        reformatted_file = file.replace("-bb", "")
        if not rebuild:
            if Path(f"{bestiary_path}{reformatted_file}").exists():
                continue

        path = Path(f"{raw_path}{file}")
        print(f"Loading {file}...")
        try:
            raw_dict = json.loads(path.read_text())
        except (json.decoder.JSONDecodeError):
            print(f"ERROR: could not decode {file}")
            continue
        
        print(f"Reformatting {file}...")
        monster = {
                "name": "",
                "level": 0,
                "traits": [],
                "perception": 0,
                "skills": {},
                "attributeModifiers": {
                    "str": 0,
                    "dex": 0,
                    "con": 0,
                    "int": 0,
                    "wis": 0,
                    "cha": 0
                },
                "defenses": {
                    "armorClass": 10,
                    "saves": {
                        "fortitude": 0,
                        "reflex": 0,
                        "will": 0
                    },
                },
                "maxHitPoints": 10,
                "immunities": [],
                "speed": 20,
                "actions": {
                    "attacks": {}
                }
            }
        monster['name'] = raw_dict['prototypeToken']['name']
        monster['level'] = raw_dict['system']['details']['level']['value']

        if raw_dict['system']['traits']['rarity'] != 'common':
            monster['traits'].append(raw_dict['system']['traits']['rarity'])
        monster['traits'].append(raw_dict['system']['traits']['size']['value'])

        traits = raw_dict['system']['traits']['value']
        for trait in traits:
            monster['traits'].append(trait)

        try:
            monster['perception'] = raw_dict['system']['perception']['mod']
        except (KeyError):
            print(f"No perception found in {monster['name']}. May be a hazard.")
            continue

        skills = raw_dict['system']['skills']
        for skill in skills:
            monster['skills'][skill] = skills[skill]['base']

        abilities = raw_dict['system']['abilities']
        for ability in abilities:
          monster['attributeModifiers'][ability] = abilities[ability]['mod']
        
        system_attributes = raw_dict['system']['attributes']
        monster['defenses']['armorClass'] = system_attributes['ac']['value']
        saves = raw_dict['system']['saves']
        for save in saves:
            monster['defenses']['saves'][save] = saves[save]['value']

        
        monster['maxHitPoints'] = system_attributes['hp']['max']
        monster['speed'] = system_attributes['speed']['value']
        if "immunities" in system_attributes:
            immunities = system_attributes['immunities']

            for immunity in immunities:
                monster['immunities'].append(immunity['type'])

        items = raw_dict['items']

        for item in items:
            if "attack" in item['system']:
                attack_dict = {}
                attack_dict['attackBonus'] = item['system']['bonus']['value']
                # for some reason in the JSON files from foundryVTT there is a
                # key with a random value between damageRolls and the values
                # inside it that I need, thus the damage_roll_key variable
                try:
                    damage_roll_key = list(item['system']['damageRolls'].keys())[0]
                    attack_dict['damage'] = item['system']['damageRolls'][damage_roll_key]['damage']
                    attack_dict['damageType'] = item['system']['damageRolls'][damage_roll_key]['damageType']
                except (IndexError):
                    pass
                monster['actions']['attacks'].update({f"{item['name']}": attack_dict})

        print(f"Saving {reformatted_file}...\n")
        path = Path(f"{bestiary_path}{reformatted_file}")
        monster_json = json.dumps(monster, indent=4)
        path.write_text(monster_json)

    print("Files reformatted.\n")

def cleanup(raw_path: str) -> None:
    print("Cleaning up...")
    shutil.rmtree(raw_path)

def main():
    rebuild = False
    parent_directory = str(Path(__file__).parent.parent)
    raw_path = f'{parent_directory}/raw_data/'
    bestiary_path = f'{parent_directory}/bestiary/'

    if len(sys.argv) == 2:
        if sys.argv[1] == "--rebuild":
            rebuild = True

    fetch_data(parent_directory, raw_path, bestiary_path, rebuild)
    convert_data(parent_directory, raw_path, bestiary_path, rebuild)
    cleanup(raw_path)
    print("Initialization complete!")

if __name__ == "__main__":
    main()