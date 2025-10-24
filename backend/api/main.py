import os
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

class Actions(BaseModel):
    attacks: dict[str, dict[str, int|str]]

class Enemy(BaseModel):
    id: int
    name: str
    level: int
    traits: list[str]
    perception: int
    skills: dict[str, int]
    attributeModifiers: dict[str, int]
    defenses: dict[str, int|dict[str, int]]
    maxHitPoints: int
    immunities: list[str]
    speed: int
    actions: Optional[Actions]

class Enemies(BaseModel):
    enemies: list[Enemy]
    
app = FastAPI(debug=True)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

enemy_list = {"enemies": []}

@app.get("/enemies", response_model=Enemies)
def get_enemies():
    if not enemy_list['enemies']:
        post_enemies()
    return Enemies(enemies=enemy_list["enemies"])

@app.post("/enemies")
def add_enemy(enemy: Enemy):
    enemy_list["enemies"].append(enemy)
    return enemy

def post_enemies():
    parent_directory = str(Path(__file__).parent.parent)
    bestiary_path = f"{parent_directory}/data/bestiary/"
    url = "http://localhost:8000/enemies"

    files=os.listdir(bestiary_path)
    files.sort()
    for file in files:
        path = Path(f"{bestiary_path}{file}")
        data = path.read_text()
        requests.post(url, data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)