from sqlalchemy.future import select

import models
from schemas import Characters


def fetch_characters_from_db(current_user, db):
    query = select(models.Character)
    query = query.where(models.Character.user_id == current_user.id)
    result = db.execute(query)
    characters = result.scalars().all()
    character_list = [e.__dict__ for e in characters]
    return Characters(characters=character_list)
