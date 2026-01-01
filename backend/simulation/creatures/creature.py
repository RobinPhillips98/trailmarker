import random
import re
from typing import Self


class Creature:
    def __init__(self, creature: dict[any]):
        # Basic Stats
        self.name: str = creature["name"]
        self.level: int = creature["level"]
        self.perception: int = creature["perception"]
        self.max_hit_points: int = creature["max_hit_points"]
        self.hit_points: int = self.max_hit_points
        self.speed: int = creature["speed"]
        self.armor_class: int = creature["defenses"]["armor_class"]

        # Attribute Modifiers
        attributes = creature["attribute_modifiers"]
        self.strength: int = attributes["strength"]
        self.constitution: int = attributes["constitution"]
        self.dexterity: int = attributes["dexterity"]
        self.intelligence: int = attributes["intelligence"]
        self.wisdom: int = attributes["wisdom"]
        self.charisma: int = attributes["charisma"]

        # Skills
        skills = creature["skills"]
        # If a skill is not specified, use the base attribute for that skill
        self.acrobatics: int = skills.get("acrobatics", self.dexterity)
        self.arcana: int = skills.get("arcana", self.intelligence)
        self.athletics: int = skills.get("athletics", self.strength)
        self.crafting: int = skills.get("crafting", self.intelligence)
        self.deception: int = skills.get("deception", self.charisma)
        self.diplomacy: int = skills.get("diplomacy", self.charisma)
        self.intimidation: int = skills.get("intimidation", self.charisma)
        self.lore: int = skills.get("lore", self.intelligence)
        self.medicine: int = skills.get("medicine", self.wisdom)
        self.nature: int = skills.get("nature", self.wisdom)
        self.occultism: int = skills.get("occultism", self.intelligence)
        self.performance: int = skills.get("performance", self.charisma)
        self.religion: int = skills.get("religion", self.wisdom)
        self.society: int = skills.get("society", self.intelligence)
        self.stealth: int = skills.get("stealth", self.dexterity)
        self.survival: int = skills.get("survival", self.wisdom)
        self.thievery: int = skills.get("thievery", self.dexterity)

        # Saving Throws
        saves = creature["defenses"]["saves"]
        self.fortitude: int = saves["fortitude"]
        self.reflex: int = saves["reflex"]
        self.will: int = saves["will"]

        # Actions
        try:
            self.attacks: dict[any] = creature["actions"]["attacks"]
        except KeyError:
            self.attacks = None

        # Encounter Data
        self.encounter = None
        self.actions: int = 3
        self.initiative: int = 0
        self.team: int = None
        self.is_dead: bool = False

    def __repr__(self) -> str:
        return self.name

    def join_encounter(self, encounter) -> None:
        self.encounter = encounter
        self.roll_initiative()

    def roll_initiative(self) -> None:
        self.initiative = 10 + self.perception

    def take_turn(self) -> None:
        if not self.encounter:
            print("Error: Turns cannot be taken outside of an encounter")
            return

        if self.team == 1:
            target = self.pick_target(self.encounter.enemies)
        if self.team == 2:
            target = self.pick_target(self.encounter.players)

        attack = self.pick_attack()

        self.attack(attack, target)

    def pick_target(self, targets: list[Self]) -> Self:
        return random.choice(targets)

    def pick_attack(self) -> dict[any]:
        return self.attacks[0]

    def attack(self, weapon: dict[str, str | int], target) -> None:
        attack_bonus = weapon["attackBonus"]

        damage_roll = weapon["damage"]
        split_string = re.split(r"d|\+", damage_roll)
        num_dice = int(split_string[0])
        die_size = int(split_string[1])
        damage_bonus = int(split_string[2]) if len(split_string) == 3 else 0

        average_roll = (die_size + 1) / 2
        average_damage = (num_dice * average_roll) + damage_bonus

        # This could be one line, but this is more readable and intuitive
        min_roll_to_hit = target.armor_class - attack_bonus
        miss_chance = min_roll_to_hit / 20
        hit_chance = 1 - miss_chance

        damage = int(average_damage * hit_chance)
        print(f"{self} attacked {target} for {damage} damage!")
        target.take_damage(damage)

    def take_damage(self, damage: int) -> None:
        self.hit_points -= damage
        # print(f"{self} took {damage} damage!")

        if self.hit_points <= 0:
            self.die()
        else:
            print(f"{self} has {self.hit_points} HP remaining!")

    def die(self) -> None:
        print(f"{self} has died!")
        self.is_dead = True
        if self.encounter:
            self.encounter.remove_creature(self)
