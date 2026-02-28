"""Defines the Enemy subclass extending Creature, and its methods."""

from typing import Any

from .creature import Creature


class Enemy(Creature):
    """An enemy the players will fight in the simulated encounter.

    Attributes:
        traits: The traits the enemy has, such as rarity and size
        immunities: The enemy's immunities to damage types and conditions
        weaknesses: A dictionary containing each weakness the enemy has to a
            damage type, and the value of that weakness
        resistances: A dictionary containing each resistance the enemy has to a
            damage type, and the value of that resistance
    """

    # Built-in Methods

    def __init__(self, enemy: dict[str, Any], simulation=None):
        """Initializes the enemy based on the passed in dictionary.

        Args:
            enemy (dict[str, Any]): The data used to build the enemy
            simulation (Simulation, optional): The simulation the creature is
                in. Defaults to None.
        """
        super().__init__(enemy, simulation)
        self.traits: list[str] = enemy["traits"]
        self.immunities: list[str] = enemy["immunities"]
        self.weaknesses: dict[str, int] = enemy.get("weaknesses", {})
        self.resistances: dict[str, int] = enemy.get("resistances", {})
        self.team = 2

        # Any skill not specified in enemy data is set to none
        # None skills need to be set to correct base amount: the base attribute
        if self.acrobatics is None:
            self.acrobatics = self.dexterity
        if self.arcana is None:
            self.arcana = self.intelligence
        if self.athletics is None:
            self.athletics = self.strength
        if self.crafting is None:
            self.crafting = self.intelligence
        if self.deception is None:
            self.deception = self.charisma
        if self.diplomacy is None:
            self.diplomacy = self.charisma
        if self.intimidation is None:
            self.intimidation = self.charisma
        if self.medicine is None:
            self.medicine = self.wisdom
        if self.nature is None:
            self.nature = self.wisdom
        if self.occultism is None:
            self.occultism = self.intelligence
        if self.performance is None:
            self.performance = self.charisma
        if self.religion is None:
            self.religion = self.wisdom
        if self.society is None:
            self.society = self.intelligence
        if self.stealth is None:
            self.stealth = self.dexterity
        if self.survival is None:
            self.survival = self.wisdom
        if self.thievery is None:
            self.thievery = self.dexterity

        if enemy["actions"]["sneak_attack"]:
            self.sneak_attack = True

    # Public Methods

    def long_description(self) -> str:
        """Gives a well-formatted description of the enemy.

        Returns:
            str: The long description of the enemy.
        """
        return f"{self}: Level {self.level}"

    def take_damage(self, damage: int, damage_type: str) -> None:
        """Subtracts `damage` from the creature's HP after modifying it.

        First, checks if the target is immune, weak, or resistant to
        `damage_type` and if so, modifies `damage` accordingly. Then, the
        modified `damage` is subtracted from the creature's current hit points,
        and if their hit points fall below 0, the creature dies and is removed
        from the encounter.

        Args:
            damage (int): The damage the creature is to take.
            damage_type (str): The type of damage being dealt, ex. fire
        """
        if damage_type in self.immunities:
            self.log(f"{self} is immune to {damage_type}. No damage taken!")
            return

        if damage_type in self.weaknesses.keys():
            extra_damage = self.weaknesses[damage_type]
            damage += extra_damage
            self.log(
                f"{self} is weak to {damage_type}, {extra_damage} extra damage taken, total {damage} damage."  # noqa: E501
            )
        elif "all-damage" in self.resistances.keys():
            damage_reduction = self.resistances["all-damage"]
            damage -= damage_reduction
            if damage <= 0:
                damage = 1
            self.log(
                f"{self} is resistant to all damage, {damage_reduction} damage resisted, total {damage} damage."  # noqa: E501
            )
        elif damage_type in self.resistances.keys():
            damage_reduction = self.resistances[damage_type]
            damage -= damage_reduction
            if damage <= 0:
                damage = 1
            self.log(
                f"{self} is resistant to {damage_type}, {damage_reduction} damage resisted, total {damage} damage."  # noqa: E501
            )

        super().take_damage(damage, damage_type)
