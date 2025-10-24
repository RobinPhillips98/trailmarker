from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    return Enemies(enemies=enemy_list["enemies"])

@app.post("/enemies")
def add_enemy(enemy: Enemy):
    enemy_list["enemies"].append(enemy)
    return enemy


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)