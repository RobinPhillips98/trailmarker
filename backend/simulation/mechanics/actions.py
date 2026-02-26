import math
import random
import re

from ..mechanics.misc import Degree, Die, calculate_dos, d6, d8, d10, d20


class Action:
    """A representation of a pathfinder action

    Attributes:
        name: The name of the action
        cost: An integer indicating the cost of the action from 1 to 3
        weight: An integer indicating how likely the action is to be selected
        traits: The list of traits the action has, ex. agile or finesse
        range: The distance at which the action can target a creature
        ranged: Whether the action can be used at a distance
        damage_type: The type of damage the action deals
        num_dice: The number of dice rolled for damage
        die_size: The number of faces on the die rolled for damage
        damage_bonus: The bonus added to the damage roll for the action
    """

    def __init__(
        self,
        name: str = "Undefined",
        cost: int = 1,
        weight: int = 0,
        traits: list[str] = [],
    ):
        self.name: str = name
        self.cost: int = cost
        self.weight: int = weight
        self.traits: list[str] = traits
        self.range: int = 5
        self.ranged: bool = False
        self.damage_type: str = ""
        self.num_dice: int = 0
        self.die_size: int = 0
        self.damage_bonus: int = 0

    def __repr__(self):
        return self.name.lower()

    def calculate_weight(
        self,
        penalty: int,
        actions_remaining: int,
        in_melee: bool = False,
        creature=None,
    ) -> int:
        if (
            self.cost > actions_remaining
            or (self.name.lower() == "raise shield" and creature.shield_raised)
            or (isinstance(self, Spell) and self.slots <= 0)
            or not self.check_valid_damage(creature)
        ):
            return -math.inf
        else:
            return self.weight

    def attack(self, attacker, target) -> bool:
        auto_hit = (
            self.name.lower() == "force barrage"
            or self.name.lower() == "force bolt"
        )
        if isinstance(self, Attack):
            attacker.log(f"{attacker} Strikes {target} with their {self}.")
        else:
            attacker.log(f"{attacker} attacks {target} with their {self}.")

        if auto_hit:
            degree_of_success = Degree.SUCCESS
        else:
            # Calculate attack roll and check for hit before calculating damage
            attack_roll = d20.roll()
            roll_display = ""
            penalty_per_attack = 4 if "agile" in self.traits else 5
            total_penalty = penalty_per_attack * attacker.multi_attack
            if isinstance(self, Attack):
                attack_total = attack_roll + self.attack_bonus - total_penalty
                roll_display = (
                    f"{attack_roll} + {self.attack_bonus}"
                    if total_penalty <= 0
                    else f"{attack_roll} + {self.attack_bonus} - {total_penalty}"  # noqa: E501
                )
                if attacker.encounter:
                    attacker.multi_attack += 1
            elif isinstance(self, Spell):
                attack_total = attack_roll + attacker.spell_attack_bonus
                roll_display = f"{attack_roll} + {attacker.spell_attack_bonus}"
            if attack_total <= 0:
                attack_total = 1

            attacker.log(
                f"{attacker} rolled {attack_total} ({roll_display}) to attack against AC {target.armor_class}."  # noqa: E501
            )

            degree_of_success = calculate_dos(
                attack_roll, attack_total, target.armor_class
            )

            if degree_of_success <= Degree.FAILURE:
                attacker.log("Miss!")
                return False

            attacker.log("Hit!")

        damage_type = self.damage_type

        damage_rolls = self._roll_for_damage()
        damage = sum(damage_rolls) + self.damage_bonus

        damage_display = " + ".join(str(roll) for roll in damage_rolls)

        if self.damage_bonus:
            damage_display += f" + {self.damage_bonus}"

        if attacker.sneak_attack and "finesse" in self.traits:
            sneak_attack_roll = d6.roll()
            damage += sneak_attack_roll
            attacker.log(
                f"{attacker} sneak attacks for {sneak_attack_roll} extra damage."  # noqa: E501
            )
            damage_display += f" + {sneak_attack_roll}"

        if degree_of_success == Degree.CRITICAL_SUCCESS:
            attacker.log(f"{attacker} dealt a critical hit to {target}!")
            damage *= 2
            damage_display += " doubled"
            if "deadly-6" in self.traits:
                deadly_roll = d6.roll()
                damage += deadly_roll
                damage_display += f" + {deadly_roll}"
            elif "deadly-8" in self.traits:
                deadly_roll = d8.roll()
                damage += deadly_roll
                damage_display += f" + {deadly_roll}"
            elif "deadly-10" in self.traits:
                deadly_roll = d10.roll()
                damage += deadly_roll
                damage_display += f" + {deadly_roll}"

        attacker.log(
            f"{attacker} dealt {damage} ({damage_display}) {damage_type} damage to {target}!"  # noqa: E501
        )
        target.take_damage(damage, damage_type)

        return True

    def check_valid_damage(self, creature, target=None) -> bool:
        """Checks if the action is using an invalid damage type.

        This primarily applies to vitality damage which only works against
        undead creatures. Basically, if an attack or spell does vitality damage
        and no potential targets are undead, we don't want to pick it.

        First, check if all targets are immune to the damage type. If so,
        damage is invalid. If not, proceed to vitality check.

        Doing the checks backwards like this is a bit more difficult to read
        and understand, but is far more efficient at runtime. This way, the
        function will return at the soonest opportunity.

        Optionally, a target can be specified, in which case the function
        checks if that specific target is immune.

        Args:
            creature (Creature): The creature using the action
            target (Creatyre, optional): The target being attacked.
                Defaults to None.

        Returns:
            bool: True if the damage is a valid type, false if not
        """
        # Not an attack or spell, don't need to worry about damage type
        if not isinstance(self, Attack) and not isinstance(self, Spell):
            return True
        # First, check if all targets are immune to the damage type:
        if creature.team == 1:  # Only enemies have immunities
            if target:
                if self.damage_type in target.immunities:
                    return False
            all_targets_immune = True
            for enemy in creature.encounter.enemies:
                if self.damage_type not in enemy.immunities:
                    all_targets_immune = False
                    break
            if all_targets_immune:
                return False

        # Doesn't deal vitality damage, no need to continue the checks
        if self.damage_type != "vitality":
            return True
        # Players can't be undead, and it is vitality damage
        if creature.team == 2:
            return False

        if target:
            if "undead" in target.traits:
                return True
            else:
                return False

        for enemy in creature.encounter.enemies:
            # We found an undead enemy, vitality damage can work
            if "undead" in enemy.traits:
                return True

        return False

    def _roll_for_damage(self) -> list[int]:
        damage_die = Die(self.die_size)
        damage_rolls = []
        for i in range(self.num_dice):
            damage_rolls.append(damage_die.roll())

        return damage_rolls


class Attack(Action):
    """A representation of an attack

    Attributes:
        attack_bonus: The bonus added to the attack roll for the attack
    """

    def __init__(self, attack_dict: dict[str, str | int]):
        self.name: str = attack_dict["name"].strip()
        self.range: int = attack_dict.get("range", 5)
        if not self.range:
            self.range = 5
        self.ranged: bool = self.range > 5
        self.attack_bonus: int = attack_dict["attackBonus"]
        self.damage_type: str = attack_dict["damageType"]
        self.traits = attack_dict.get("traits", [])

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

    def calculate_weight(
        self,
        penalty: int,
        actions_remaining: int,
        in_melee: bool = False,
        creature=None,
    ) -> int:
        base_weight = super().calculate_weight(
            penalty, actions_remaining, in_melee, creature
        )
        if math.isinf(base_weight):
            return base_weight
        if in_melee and self.ranged:
            return 0

        penalty_per_attack = 4 if "agile" in self.traits else 5
        total_penalty = penalty_per_attack * penalty

        effective_weight = base_weight - total_penalty
        if total_penalty >= 8:  # a third attack is almost always a bad option
            effective_weight *= 0.5

        return effective_weight


class Spell(Action):
    """A representation of a spell in Pathfinder

    Attributes:
        slots: The number of slots the spell is prepared in
        level: The level of the spell
        area_type: The type of area the spell has, such as a burst, if any
        area_size: The size of the spell's area, such as a radius, if any
        save: The saving throw used to defend against the spell, if any
        targets: The number of creatures the spell can target, if any
    """

    def __init__(
        self, spell_dict: dict[str, str | int | dict[str, str]], bonus: int = 0
    ):
        self.name: str = spell_dict["name"].strip()
        self.slots: int = spell_dict["slots"]
        self.level: int = spell_dict["level"]
        self.bonus: int = bonus
        self.traits: list[str] = []

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
            + self.area_size * 3
            + self.targets
        )

        if self.range:
            self.weight += self.range / 5

    def calculate_weight(
        self,
        penalty: int,
        actions_remaining: int,
        in_melee: bool = False,
        creature=None,
    ) -> int:
        base_weight = super().calculate_weight(
            penalty, actions_remaining, in_melee, creature
        )
        if math.isinf(base_weight):
            return base_weight

        if self.level == 0:
            weight = base_weight * 1.5
        else:
            weight = base_weight * self.slots

        auto_hit = (
            self.name.lower() == "force barrage"
            or self.name.lower() == "force bolt"
        )
        if auto_hit:
            weight += 20
        else:
            weight += self.bonus

        return weight

    def cast(self, caster) -> None:
        if self.targets:
            targets = []

            # Pick best target and move to them
            first_target = caster.pick_target(self)
            targets.append(first_target)
            caster.move_to(first_target, self.range)
            if caster.num_actions <= self.cost:
                return

            caster.log(f"{caster} casts {self}!")
            # Pick remaining targets
            for i in range(self.targets - 1):
                target = caster.pick_target(self)
                targets.append(target)
            for target in targets:
                self.attack(caster, target)
        elif self.area_size:
            caster.log(f"{caster} casts {self}!")
            self._aoe(caster)

        if self.level >= 1:
            self.slots -= 1

    def _aoe(self, caster):
        # AOE spells calculate an abstract number of targets
        # May modify to use map in the future
        num_targets = 0
        match self.area_type:
            case "burst":
                num_targets = math.ceil(self.area_size / 5)
            case "cone":
                num_targets = math.ceil(self.area_size / 10)
            case "emanation":
                num_targets = math.ceil(self.area_size / 5)
            case "line":
                num_targets = math.ceil(self.area_size / 30)
            case _:
                raise Exception("Invalid spell area type")

        opponents = (
            caster.encounter.enemies
            if caster.team == 1
            else caster.encounter.players
        )
        if num_targets <= len(opponents):
            targets = random.sample(opponents, num_targets)
        else:
            targets = opponents

        damage_rolls = self._roll_for_damage()
        damage = sum(damage_rolls) + self.damage_bonus

        target_names = ", ".join(map(str, targets))
        caster.log(f"{caster} attacks {target_names} with {self}!")
        for target in targets:
            target.spell_save(damage, self, caster)
