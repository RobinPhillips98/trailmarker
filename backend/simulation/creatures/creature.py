import random
from typing import Self

from ..mechanics.actions import Attack
from ..mechanics.dice import Die, d20


class Creature:
    """A creature, such as a player or enemy, ready for use in an encounter.

    A representation of a creature from Pathfinder 2E with support for basic
    stats, attribute modifiers, skills, saving throws as well as methods
    for taking turns, attacking, and taking damage. For sake of brevity,
    only non-obvious attributes will be explained.

    Attributes:
        attacks: A list of dictionaries containing information on each of the
            creature's available weapon attacks.
        encounter: The encounter the creature is in, if any, primarily used
            for removing the creature from the encounter on death.
        team: 1 if the creature is a player, 2 if the creature is an enemy.
        simulation: The simulation the creature is in, if any, primarily used
            for adding to the simulation's combat log.
    """

    # Built-in Methods

    def __init__(self, creature: dict[any], simulation=None):
        """Initializes the creature based on the given dictioanry

        Args:
            creature (dict[any]): Data used to build the Creature.
            simulation (Simulation, optional): The simulation the creature is
                in. Defaults to None.
        """
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
        self.attacks: list[Attack] = []
        try:
            for attack_dict in creature["actions"]["attacks"]:
                attack = Attack(attack_dict)
                self.attacks.append(attack)
        except KeyError:
            self.attacks = None

        # Encounter Data
        self.encounter = None
        self.initiative: int = 0
        self.actions: int = 0
        self.map: int = 0  # Multi-attack Penalty
        self.team: int = None
        self.is_dead: bool = False

        # Simulation Data
        self.simulation = simulation

    def __repr__(self) -> str:
        return self.name

    # Public Methods

    def join_encounter(self, encounter) -> None:
        """Sets the creature's encounter and rolls initiative.

        Args:
            encounter (Encounter): The encounter for the creature to join
        """
        self.encounter = encounter
        self._roll_initiative()

    def take_turn(self) -> None:
        """The creature picks a target at random and attacks that target."""
        if not self.encounter:
            print("Error: Turns cannot be taken outside of an encounter")
            return

        self._log(f"{self}'s turn:")
        self.actions = 3
        self.map = 0

        # TODO: Proper movement
        self.actions -= 1  # Simulating at least one action spent on movement

        while self.actions > 0:
            if self.encounter.players and self.encounter.enemies:
                self._perform_action()
            else:
                break

    def take_damage(self, damage: int) -> None:
        """Subtracts the given damage from the creature's HP.

        The given damage is subtracted from the creature's current hit points,
        and if their hit points fall below 0, the creature dies.

        Args:
            damage (int): The damage the creature is to take.
        """
        self.hit_points -= damage

        if self.hit_points <= 0:
            self._die()
        else:
            self._log(f"{self} has {self.hit_points} HP remaining!")

    # Private Methods

    def _roll_initiative(self) -> None:
        self.initiative = d20.roll() + self.perception

    def _perform_action(self):
        if self.team == 1:
            target = self._pick_target(self.encounter.enemies)
        elif self.team == 2:
            target = self._pick_target(self.encounter.players)

        attack = self._pick_attack()

        self._attack(attack, target)

        self.actions -= attack.cost

    def _pick_target(self, targets: list[Self]) -> Self:
        return random.choice(targets)

    def _pick_attack(self) -> dict[any]:
        return self.attacks[0]

    def _attack(self, attack: Attack, target: Self) -> bool:
        self._log(f"{self} is attacking {target} with their {attack}.")

        # Calculate attack roll and check for hit before calculating damage
        attack_roll = d20.roll()
        attack_total = attack_roll + attack.attack_bonus - self.map
        self._log(f"{self} rolled {attack_total} to attack.")
        if self.encounter:
            self.map += 5

        if attack_total < target.armor_class:
            self._log("Miss!")
            return False

        damage_type = attack.damage_type
        damage_roll = Die(attack.die_size).roll()
        damage = (attack.num_dice * damage_roll) + attack.damage_bonus

        self._log("Hit!")
        self._log(f"{self} dealt {damage} {damage_type} damage to {target}!")
        target.take_damage(damage)

        return True

    def _die(self) -> None:
        self._log(f"{self} has died!")
        self.is_dead = True
        if self.encounter:
            self.encounter.remove_creature(self)

    def _log(self, message: str = ""):
        if self.simulation:
            self.simulation.log(message)
        else:
            print(message)
