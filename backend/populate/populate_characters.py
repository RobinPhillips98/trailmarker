import json
import os
from pathlib import Path

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import Character, User


def initialize_characters(db: Session):
    user = db.execute(select(User).filter(User.username == "admin")).scalar()
    data_folder = "populate/data/"
    filenames = os.listdir(data_folder)
    for filename in filenames:
        path = Path(f"{data_folder}/{filename}")
        character_dict = json.loads(path.read_text())
        db_character = Character(
            user=user,
            name=character_dict["name"],
            xp=0,
            ancestry=character_dict["ancestry"],
            heritage=character_dict["heritage"],
            background=character_dict["background"],
            class_=character_dict["class"],
            level=character_dict["level"],
            perception=character_dict["perception"],
            skills=character_dict["skills"],
            attribute_modifiers=character_dict["attribute_modifiers"],
            defenses=character_dict["defenses"],
            max_hit_points=character_dict["max_hit_points"],
            spell_attack_bonus=character_dict.get("spell_attack_bonus"),
            spell_dc=character_dict.get("spell_dc"),
            speed=character_dict["speed"],
            actions=character_dict["actions"],
        )
        db.add(db_character)

    db.commit()
