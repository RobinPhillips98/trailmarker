import json
import os
from pathlib import Path

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from api.character_helpers import convert_to_db_character
from models import User
from schemas import CharacterCreate


def initialize_characters(db: Session):
    user = db.execute(select(User).filter(User.username == "admin")).scalar()
    data_folder = "data/characters/"
    filenames = os.listdir(data_folder)
    for filename in filenames:
        path = Path(f"{data_folder}{filename}")
        character_dict = json.loads(path.read_text())
        character = CharacterCreate.model_validate(
            character_dict, by_alias=True
        )
        db_character = convert_to_db_character(character, user)
        db.add(db_character)

    db.commit()
