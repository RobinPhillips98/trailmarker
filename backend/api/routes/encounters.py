from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.orm import Session

import models

from ..dependencies import get_db

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


class Encounter(BaseModel):
    id: int
    name: str
    enemies: list[dict[str, int]]


class Encounters(BaseModel):
    encounters: list[Encounter]


@router.get("/encounters", response_model=Encounters, status_code=status.HTTP_200_OK)
def get_encounters(db: db_dependency):
    query = select(models.Encounter)
    result = db.execute(query)
    encounters = result.scalars().all()
    encounter_list = [e.__dict__ for e in encounters]
    return Encounters(encounters=encounter_list)


@router.get("/encounters/{encounter_id}", response_model=Encounter, status_code=status.HTTP_200_OK)
def get_encounter(encounter_id, db: db_dependency):
    query = db.query(models.Encounter).where(models.Encounter.id == encounter_id)

    result = db.execute(query)
    encounter = result.scalars().first()

    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found")

    return encounter


@router.post("/encounters", response_model=Encounter, status_code=status.HTTP_201_CREATED)
def add_encounter(encounter: Encounter, db: db_dependency):
    try:
        db_encounter = models.Encounter(
            name=encounter.name,
            enemies=encounter.enemies
        )
        db.add(db_encounter)
        db.commit()
        db.refresh(db_encounter)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Error in add_enemy: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        )
    return encounter


@router.delete("/encounters/{encounter_id}", response_model=object, status_code=status.HTTP_200_OK)
def delete_encounter(encounter_id, db: db_dependency):
    query = db.query(models.Encounter).where(models.Encounter.id == encounter_id)

    result = db.execute(query)
    encounter = result.scalars().first()

    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found")

    db.delete(encounter)
    db.commit()

    return {"message": "Encounter deleted"}
