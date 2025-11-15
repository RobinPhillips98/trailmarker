from typing import Optional

from pydantic import BaseModel


# Encounters
class Encounter(BaseModel):
    id: int
    name: str
    enemies: list[dict[str, str | int]]


class Encounters(BaseModel):
    encounters: list[Encounter]


# Stats
class Actions(BaseModel):
    attacks: dict[str, dict[str, int | str]]


class Skills(BaseModel):
    acrobatics: Optional[int] = None
    arcana: Optional[int] = None
    athletics: Optional[int] = None
    crafting: Optional[int] = None
    deception: Optional[int] = None
    diplomacy: Optional[int] = None
    intimidation: Optional[int] = None
    lore: Optional[int] = None
    medicine: Optional[int] = None
    nature: Optional[int] = None
    occultism: Optional[int] = None
    performance: Optional[int] = None
    religion: Optional[int] = None
    society: Optional[int] = None
    stealth: Optional[int] = None
    survival: Optional[int] = None
    thievery: Optional[int] = None


class Saves(BaseModel):
    fortitude: int
    reflex: int
    will: int


class Defenses(BaseModel):
    armor_class: int
    saves: Saves


class Attributes(BaseModel):
    strength: int
    constitution: int
    dexterity: int
    intelligence: int
    wisdom: int
    charisma: int


# Creatures
class Creature(BaseModel):
    id: int
    name: str
    level: int
    traits: list[str]
    perception: int
    skills: Skills
    attribute_modifiers: Attributes
    defenses: Defenses
    max_hit_points: int
    speed: int
    actions: Optional[Actions]


class Enemy(Creature):
    immunities: list[str]


class Enemies(BaseModel):
    enemies: list[Enemy]


# Authentication
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str


class UserInDB(UserResponse):
    hashed_password: str
