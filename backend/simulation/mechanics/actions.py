import re


class Action:
    """A representation of a pathfinder action

    Attributes:
        cost: An integer indicating the cost of the action from 1 to 3
        weight: An integer indicating how likely the action is to be selected
    """

    def __init__(self, cost=1, weight=0):
        self.cost: int = cost
        self.weight: int = weight


class Attack(Action):
    """A representation of an attack

    Attributes:
        name: The name of the attack
        attack_bonus: The bonus added to the attack roll for the attack
        damage_type: The type of damage the attack deals
        num_dice: The number of dice rolled for damage
        die_size: The number of faces on the die rolled for damage
        damage_bonus: The bonus added to the damage roll for the attack
        cost: An integer indicating the cost of the action from 1 to 3
        weight: An integer indicating how likely the action is to be selected
    """

    def __init__(self, attack_dict: dict[any]):
        self.name: str = attack_dict["name"]
        self.attack_bonus: int = attack_dict["attackBonus"]
        self.damage_type: str = attack_dict["damageType"]

        # Due to regex verification on frontend, damage will always be listed
        # in the form "XdY" or "XdY±Z", so split on d, +, and - in order to
        # isolate the individual numbers needed
        damage_roll_string = attack_dict["damage"]
        split_string = re.split(r"d|\+|-", damage_roll_string)
        self.num_dice: int = int(split_string[0])
        self.die_size: int = int(split_string[1])
        self.damage_bonus: int = (
            int(split_string[2]) if len(split_string) == 3 else 0
        )

        self.cost: int = 1
        self.weight: int = (
            (self.num_dice * self.die_size)
            + self.damage_bonus
            + self.attack_bonus
        )

    def __repr__(self):
        return self.name.lower()
