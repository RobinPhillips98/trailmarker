from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# Encounters
class Encounter(BaseModel):
    id: int
    name: str
    enemies: list[dict[str, str | int]]


class Encounters(BaseModel):
    encounters: list[Encounter]


# Stats
class Attack(BaseModel):
    name: str
    attackBonus: int
    damage: Optional[str] = None
    damageType: Optional[str] = None
    range: Optional[int] = None


class Spell(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    name: str
    slots: int
    level: int
    damage_roll: str
    damage_type: str
    range_: str = Field(..., alias="range")
    area: Optional[dict[str, str | int]] = None
    save: Optional[str] = "none"
    target: str
    actions: str


class Actions(BaseModel):
    attacks: Optional[list[Attack]] = None
    spells: Optional[list[Spell]] = None


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
    perception: int
    skills: Skills
    attribute_modifiers: Attributes
    defenses: Defenses
    max_hit_points: int
    spell_attack_bonus: Optional[int] = None
    spell_dc: Optional[int] = None
    speed: int
    actions: Optional[Actions]


class Character(Creature):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    user_id: int
    player: Optional[str] = ""
    xp: Optional[int] = 0
    ancestry: str
    background: str
    class_: str = Field(..., alias="class")


class Enemy(Creature):
    traits: list[str]
    immunities: list[str]
    weaknesses: dict[str, int]
    resistances: dict[str, int]


class CreatureCreate(BaseModel):
    name: str
    level: int
    perception: int
    skills: Skills
    attribute_modifiers: Attributes
    defenses: Defenses
    max_hit_points: int
    spell_attack_bonus: Optional[int] = None
    spell_dc: Optional[int] = None
    speed: int
    actions: Optional[Actions]


class CreatureUpdate(BaseModel):
    id: int
    name: str
    level: int
    perception: int
    skills: Skills
    attribute_modifiers: Attributes
    defenses: Defenses
    max_hit_points: int
    spell_attack_bonus: Optional[int] = None
    spell_dc: Optional[int] = None
    speed: int
    actions: Optional[Actions]


class EnemyCreate(CreatureCreate):
    traits: list[str]
    immunities: list[str]


class CharacterCreate(CreatureCreate):
    model_config = ConfigDict(populate_by_name=True)

    player: Optional[str] = ""
    xp: Optional[int] = 0
    ancestry: str
    background: str
    class_: str = Field(..., alias="class")


class CharacterUpdate(CreatureUpdate):
    model_config = ConfigDict(populate_by_name=True)

    player: Optional[str] = ""
    xp: Optional[int] = 0
    ancestry: str
    background: str
    class_: str = Field(..., alias="class")


class Enemies(BaseModel):
    enemies: list[Enemy]


class Characters(BaseModel):
    characters: list[Character]


# Simulation
class SimEnemyInfo(BaseModel):
    id: int
    quantity: int


class SimRequest(BaseModel):
    enemies: list[SimEnemyInfo]


class SimData(BaseModel):
    winner: str
    rounds: int
    players_killed: int
    total_players: int
    sim_num: int
    log: list[str]


class SimResponse(BaseModel):
    wins: int
    total_sims: int
    sim_data: list[SimData]


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
