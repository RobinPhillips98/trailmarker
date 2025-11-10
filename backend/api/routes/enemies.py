from typing import Annotated, Optional
import json
from pathlib import Path
import os

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
import requests
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.future import select

import models
from ..dependencies import get_db

router = APIRouter()

db = Annotated[Session, Depends(get_db)]

class Actions(BaseModel):
    attacks: dict[str, dict[str, int|str]]

    def toJSON(self):
        return json.dumps(
            self,
            default =lambda o: o.__dict__,
            sort_keys=True,
            indent=4
        )

class Enemy(BaseModel):
    id: int
    name: str
    level: int
    traits: list[str]
    perception: int
    skills: dict[str, int]
    attribute_modifiers: dict[str, int]
    defenses: dict[str, int|dict[str, int]]
    max_hit_points: int
    immunities: list[str]
    speed: int
    # actions: Optional[Actions]

class Enemies(BaseModel):
    enemies: list[Enemy]

@router.get(
    "/enemies",
    response_model=Enemies,
    status_code=status.HTTP_200_OK
)
def get_enemies(db: db):
    first_row = db.query(models.Enemy).first()
    if not first_row:
        post_enemies()
    query = select(models.Enemy)
    result = db.execute(query)
    enemies = result.scalars().all()
    enemy_list = [e.__dict__ for e in enemies]
    return Enemies(enemies=enemy_list)

@router.post(
    "/enemies",
    response_model=Enemy,
    status_code=status.HTTP_201_CREATED
)
async def add_enemy(enemy: Enemy, db: db):
    try:
        db_enemy = models.Enemy(
            name = enemy.name,
            level = enemy.level,
            traits = enemy.traits,
            perception = enemy.perception,
            skills = enemy.skills,
            attribute_modifiers = enemy.attribute_modifiers,
            defenses = enemy.defenses,
            max_hit_points = enemy.max_hit_points,
            immunities = enemy.immunities,
            speed = enemy.speed,
            # actions = enemy.actions.toJSON()
        )

        db.add(db_enemy)
        db.commit()
        db.refresh(db_enemy)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(F"Error in add_enemy: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    return enemy

def post_enemies():
    root_directory = str(Path(__file__).parent.parent.parent)
    bestiary_path = f"{root_directory}/data/bestiary/"
    url = "http://localhost:8000/enemies"

    files=os.listdir(bestiary_path)
    files.sort()
    for file in files:
        path = Path(f"{bestiary_path}{file}")
        data = path.read_text()
        requests.post(url, data)
