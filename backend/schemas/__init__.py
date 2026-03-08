"""Defines the pydantic models used throughout the API."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BasicResponse(BaseModel):
    message: str


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
    traits: Optional[list[str]] = []


class Spell(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    name: str
    slots: int
    level: int
    damage_roll: str
    damage_type: str
    range_: int = Field(..., alias="range")
    area: Optional[dict[str, str | int]] = None
    save: Optional[str] = None
    targets: Optional[int] = 0
    actions: str


class Actions(BaseModel):
    attacks: Optional[list[Attack]] = None
    spells: Optional[list[Spell]] = None
    heals: Optional[int] = None
    shield: Optional[int] = 0
    sneak_attack: Optional[bool] = False


class ActionsRequest(BaseModel):
    attacks: Optional[list[str]] = []
    # spells: Optional[list[str]] = []
    spells: Optional[list[Spell]] = None
    heals: Optional[int] = None
    shield: Optional[int] = 0
    sneak_attack: Optional[bool] = False


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
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

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
    heritage: str
    background: str
    class_: str = Field(..., alias="class")
    proficiencies: Optional[dict[str, int]] = {}
    extra_proficiencies: Optional[dict[str, int]] = {}
    other_features: Optional[list[str]] = []


class Enemy(Creature):
    traits: list[str]
    immunities: list[str]
    weaknesses: dict[str, int]
    resistances: dict[str, int]


class CharacterCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

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
    actions: Optional[ActionsRequest]
    player: Optional[str] = ""
    xp: Optional[int] = 0
    ancestry: str
    heritage: str
    background: str
    class_: str = Field(..., alias="class")
    proficiencies: Optional[dict[str, int]] = {}
    extra_proficiencies: Optional[dict[str, int]] = {}
    other_features: Optional[list[str]] = []


class CharacterUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

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
    actions: Optional[ActionsRequest]
    player: Optional[str] = ""
    xp: Optional[int] = 0
    ancestry: str
    heritage: str
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
    total_sims: int
    wins: int
    wins_ratio: float
    average_deaths: float
    average_rounds: float
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


class UserUpdate(BaseModel):
    username: Optional[str] = None
    old_password: str
    password: Optional[str] = None


class UserDelete(BaseModel):
    password: str


class UserResponse(BaseModel):
    username: str


class UserInDB(UserResponse):
    hashed_password: str


# Pathbuilder Schemas
class PathbuilderAbilities(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
    str_: int = Field(..., alias="str")
    dex: int
    con: int
    wis: int
    cha: int
    int_: int = Field(..., alias="int")


class PathbuilderAttributes(BaseModel):
    ancestryhp: int
    classhp: int
    bonushp: int
    bonushpPerLevel: int
    speed: int


class PathbuilderProfiencies(BaseModel):
    perception: int
    fortitude: int
    reflex: int
    will: int
    simple: int
    martial: int
    acrobatics: int
    arcana: int
    athletics: int
    crafting: int
    deception: int
    diplomacy: int
    intimidation: int
    medicine: int
    nature: int
    occultism: int
    performance: int
    religion: int
    society: int
    stealth: int
    survival: int
    thievery: int


class PathbuilderWeapon(BaseModel):
    name: str
    # qty: int
    # die: str
    # damageType: str
    # attack: int
    # damageBonus: int


class PathbuilderArmor(BaseModel):
    acTotal: int
    shieldBonus: int


class PathbuilderImport(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    name: str
    class_: str = Field(..., alias="class")
    level: int
    xp: int
    ancestry: str
    heritage: str
    background: str
    abilities: PathbuilderAbilities
    attributes: PathbuilderAttributes
    proficiencies: PathbuilderProfiencies
    lores: list[list[str | int]]
    weapons: list[PathbuilderWeapon]
    acTotal: PathbuilderArmor
