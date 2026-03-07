"""Defines helper functions used by multiple modules in the API."""

from sqlalchemy.future import select

import models
from schemas import Characters


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
