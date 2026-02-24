import re
from math import inf


class Action:
    """A representation of a pathfinder action

    Attributes:
        cost: An integer indicating the cost of the action from 1 to 3
        weight: An integer indicating how likely the action is to be selected
    """

    def __init__(self, name=None, cost=1, weight=0):
        self.name: str = name
        self.cost: int = cost
        self.weight: int = weight
        self.range: int = 5
        self.ranged: bool = False

    def calculate_weight(
        self, penalty: int, actions_remaining: int, in_melee: bool = False
    ) -> int:
        if self.cost > actions_remaining:
            return -inf

            return self.weight


class Attack(Action):
    """A representation of an attack

    Attributes:
        name: The name of the attack
        attack_bonus: The bonus added to the attack roll for the attack
        damage_type: The type of damage the attack deals
        num_dice: The number of dice rolled for damage
        die_size: The number of faces on the die rolled for damage
        damage_bonus: The bonus added to the damage roll for the attack
        cost: An integer indicating the cost of the attack from 1 to 3
        weight: An integer indicating how likely the attack is to be selected
    """

    def __init__(self, attack_dict: dict[str, str | int]):
        self.name: str = attack_dict["name"].strip()
        self.attack_bonus: int = attack_dict["attackBonus"]
        self.damage_type: str = attack_dict["damageType"]
        self.range: int = attack_dict.get("range", 5)
        self.ranged: bool = self.range > 5

        # Due to regex verification on frontend, damage will always be listed
        # in the form "XdY" or "XdY±Z", so split on d, +, and - in order to
        # isolate the individual numbers needed
        damage_roll_string = attack_dict["damage"]
        split_string = re.split(r"d|\+|-", damage_roll_string)
        self.num_dice: int = int(split_string[0])
        self.die_size: int = int(split_string[1])
        if len(split_string) == 3:
            self.damage_bonus: int = int(split_string[2])
        else:
            self.damage_bonus: int = 0

        self.cost: int = 1
        self.weight: int = (
            (self.num_dice * self.die_size)
            + self.damage_bonus
            + self.attack_bonus
            + self.range / 10
        )

    def __repr__(self):
        return self.name.lower()

    def calculate_weight(
        self, penalty: int, actions_remaining: int, in_melee: bool = False
    ) -> int:
        if self.cost > actions_remaining:
            return -inf
        if in_melee and self.ranged:
            return 0

        effective_weight = self.weight - penalty
        if penalty >= 8:  # a third attack is almost always a bad option
            effective_weight *= 0.5

        return effective_weight


class Spell(Action):
    """A representation of a spell in Pathfinder

    Attributes:
        name: The name of the spell
        slots: The number of slots the spell is prepared in
        level: The level of the spell
        num_dice: The number of dice rolled for damage
        die_size: The number of faces on the die rolled for damage
        damage_bonus: The bonus added to the damage roll for the spell
        damage_type: The type of damage the spell deals
        range: The range, in feet, of the spell, if any
        area_type: The type of area the spell has, such as a burst, if any
        area_size: The size of the spell's area, such as a radius, if any
        save: The saving throw used to defend against the spell, if any
        targets: The number of creatures the spell can target, if any
        cost: An integer indicating the cost of the spell from 1 to 3
        weight: An integer indicating how likely the spell is to be selected
    """

    def __init__(
        self, spell_dict: dict[str, str | int | dict[str, str]], bonus: int
    ):
        self.name: str = spell_dict["name"].strip()
        self.slots: int = spell_dict["slots"]
        self.level: int = spell_dict["level"]
        self.bonus = bonus

        damage_roll_string = spell_dict["damage_roll"]
        split_string = re.split(r"d|\+|-", damage_roll_string)
        self.num_dice: int = int(split_string[0])
        self.die_size: int = int(split_string[1])
        if len(split_string) == 3:
            self.damage_bonus: int = int(split_string[2])
        else:
            self.damage_bonus: int = 0

        self.damage_type: str = spell_dict["damage_type"]

        range_ = spell_dict["range"].lower().strip()
        if not range_ or range_ == "none" or range_ == "melee":
            self.range: int = 5
        else:
            self.range: int = int(range_.split()[0])

        self.ranged: bool = self.range > 5

        try:
            area_dict = spell_dict["area"]
            if area_dict:
                self.area_type: str = area_dict["type"]
                area_value = area_dict["value"]
                if isinstance(area_value, str):
                    self.area_size: int = int(area_value.split()[0])
                else:
                    self.area_size: int = area_value
            else:
                self.area_type: str = None
                self.area_size: int = 0
        except KeyError:
            self.area_type: str = None
            self.area_size: int = 0

        try:
            self.save: str = spell_dict["save"]
        except KeyError:
            self.save: str = None

        try:
            target = spell_dict["target"].lower().strip()
            if not target or target == "none" or target == "n/a":
                self.targets: int = 0
            else:
                self.targets: int = int(target.split()[0])
        except KeyError:
            self.targets: int = 0

        self.cost: int = int(spell_dict["actions"].split()[0])
        self.weight: int = (
            (self.num_dice * self.die_size)
            + self.damage_bonus
            + self.area_size
            + self.targets
        )

        if self.range:
            self.weight += self.range / 5

    def __repr__(self):
        return self.name.lower()

    def calculate_weight(
        self, penalty: int, actions_remaining: int, in_melee: bool = False
    ) -> int:
        if self.cost > actions_remaining or self.slots == 0:
            return -inf
        if self.level == 0:
            weight = self.weight * 1.5
        else:
            weight = self.weight * self.slots

        auto_hit = (
            self.name.lower() == "force barrage"
            or self.name.lower() == "force bolt"
        )
        if auto_hit:
            weight += 20
        else:
            weight += self.bonus

        return weight


# TODO: Healing
