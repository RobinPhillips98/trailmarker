"""Defines the Creature class and its methods."""

import math
from typing import Any, Self

from ..mechanics.actions import Action, Attack, Spell
from ..mechanics.heal import Heal
from ..mechanics.misc import Degree, calculate_dos, d20


class Creature:
    """A creature, such as a player character or enemy.

    A full representation of a Pathfinder 2E creature with support for basic
    stats, attribute modifiers, skills, saving throws, and actions, as well as
    methods for taking turns, moving, picking targets, attacking, casting
    spells, and taking damage.

    Attributes:
        name: The creature's name.
        level: The creature's level, a measure of its overall power, and used
            in targeting weight calculations.
        perception: The creature's Perception modifier, used for initiative.
        max_hit_points: The creature's maximum hit points.
        current_hit_points: The creature's current hit points, initialized
            to max_hit_points and reduced by damage taken.
        speed: The creature's movement speed in feet per turn.
        armor_class: The creature's Armor Class, the DC attackers must meet
            or exceed to hit the creature.
        spell_attack_bonus: The bonus added to the creature's spell attack
            rolls, if the creature is a spellcaster.
        spell_dc: The DC enemies must meet or exceed on saves against the
            creature's spells, if the creature is a spellcaster.

        attribute_modifiers: The six core PF2E attribute modifiers —
            strength, dexterity, constitution, intelligence, wisdom, and
            charisma — each stored as an individual integer attribute.

        skills: The creature's skill modifiers for all standard PF2E skills.
            If a skill is not explicitly defined, it defaults to the modifier
            of its governing attribute.

        fortitude: The creature's Fortitude saving throw modifier.
        reflex: The creature's Reflex saving throw modifier.
        will: The creature's Will saving throw modifier.

        attacks: A list of Attack objects representing the creature's weapon
            attacks.
        spells: A list of Spell objects representing the creature's spells,
            if any.
        heals: The number of heal spells the creature has prepared, if any.
        shield_value: The AC bonus granted when the creature raises its
            shield, if it has one.
        actions: A combined list of all Action objects available to the
            creature, including attacks, spells, heals, and shield actions.
        sneak_attack: Whether the creature has the sneak attack ability.

        encounter: The encounter the creature is in, if any, primarily used
            for removing the creature from the encounter on death.
        initiative: The creature's initiative roll result, calculated at the
            beginning of an encounter to determine turn order.
        num_actions: The number of actions remaining in the creature's
            current turn, set to 3 at the start of each turn.
        multi_attack: The number of attacks the creature has made this turn.
        team: 1 if the creature is a player character, 2 if it is an enemy.
        is_dead: Whether the creature has been reduced to 0 hit points and
            removed from the encounter.
        shield_raised: Whether the creature currently has its shield raised,
            granting its shield_value bonus to armor_class.

        simulation: The simulation the creature is in, if any, primarily used
            for adding messages to the simulation's combat log.

        position_x: The creature's current x-coordinate on the encounter map,
            measured in 5-foot squares.
        position_y: The creature's current y-coordinate on the encounter map,
            measured in 5-foot squares.
    """

    # Built-in Methods

    def __init__(self, creature_dict: dict[str, Any], simulation=None):
        """Initializes the creature based on the values in `creature_dict`

        Args:
            creature_dict (dict[str, Any]): Data used to build the Creature.
            simulation (Simulation, optional): The simulation the creature is
                in. Defaults to None.
        """
        # Basic Stats
        self.name: str = creature_dict["name"]
        self.level: int = creature_dict["level"]
        self.perception: int = creature_dict["perception"]
        self.max_hit_points: int = creature_dict["max_hit_points"]
        self.current_hit_points: int = self.max_hit_points
        self.speed: int = creature_dict["speed"]
        self.armor_class: int = creature_dict["defenses"]["armor_class"]
        self.spell_attack_bonus: int = creature_dict.get("spell_attack_bonus")
        self.spell_dc: int = creature_dict.get("spell_dc")

        # Attribute Modifiers
        attributes = creature_dict["attribute_modifiers"]
        self.strength: int = attributes["strength"]
        self.constitution: int = attributes["constitution"]
        self.dexterity: int = attributes["dexterity"]
        self.intelligence: int = attributes["intelligence"]
        self.wisdom: int = attributes["wisdom"]
        self.charisma: int = attributes["charisma"]

        # Skills
        skills = creature_dict["skills"]
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
        saves = creature_dict["defenses"]["saves"]
        self.fortitude: int = saves["fortitude"]
        self.reflex: int = saves["reflex"]
        self.will: int = saves["will"]

        # Actions
        self.attacks: list[Attack] = []
        try:
            attack_dicts = creature_dict["actions"]["attacks"]
        except KeyError:
            self.attacks = None
        else:
            for attack_dict in attack_dicts:
                try:
                    attack = Attack(attack_dict)
                    self.attacks.append(attack)
                except KeyError as e:
                    print(f"Invalid attack: {attack_dict}, {e}")
                    continue

        self.spells: list[Spell] = []
        try:
            spell_dicts = creature_dict["actions"]["spells"]
        except KeyError:
            self.spells = None
        else:
            for spell_dict in spell_dicts:
                spell = Spell(spell_dict, self.spell_attack_bonus)
                self.spells.append(spell)

        try:
            self.heals: int = creature_dict["actions"].get("heals")
        except KeyError:
            self.heals: int = None

        try:
            self.shield_value: int = creature_dict["actions"].get("shield")
        except KeyError:
            self.shield_value: int = None

        self.actions: list[Action] = []
        if "actions" in creature_dict.keys():
            if self.attacks:
                self.actions.extend(self.attacks)
            if self.spells:
                self.actions.extend(self.spells)
            if self.heals:
                heal = Heal(self.heals)
                self.actions.append(heal)
            if self.shield_value:
                raise_shield = Action(name="Raise Shield", weight=10)
                self.actions.append(raise_shield)

        self.sneak_attack = False

        # Encounter Data
        self.encounter = None
        self.initiative: int = 0
        self.num_actions: int = 0
        self.multi_attack: int = 0
        self.team: int = 0
        self.is_dead: bool = False
        self.shield_raised: bool = False

        # Simulation Data
        self.simulation = simulation

        # Map Data
        self.position_x: int = 0
        self.position_y: int = 0

    def __repr__(self) -> str:
        """Returns the creature's name"""
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
        """The creature picks an action and performs that action.

        The creature selects its action with the highest weight and performs
        that action. If the action requires a target, it will pick the target
        with the highest weight and move to that target if necessary.
        """
        if not self.encounter:
            raise Exception("Turns cannot be taken outside of an encounter")

        if self.is_dead:
            return

        self.log(f"{self}'s turn:")
        self.log(f"{self}'s current hit points: {self.current_hit_points}")
        if not self.actions:
            self.log(f"{self} has no valid actions. Skipping turn")
            return
        self.num_actions = 3
        self.multi_attack = 0

        if self.shield_raised:
            self.shield_raised = False
            self.armor_class -= self.shield_value

        while self.num_actions > 0:
            if self.encounter.players and self.encounter.enemies:
                self._perform_action()
            else:
                break

    def calculate_weight(
        self, attacker: Self, attack: Action, consider_distance: bool
    ) -> int:
        """Calculates how valuable a target the creature is.

        Takes into account how much damage the creature has taken, and the
        creature's level. If consider_distance is true it reduces the weight
        by the number of squares between the attacker and this creature. If
        the creature is an enemy, it modifies the weight depending on whether
        the creature is immune, resistant, or weak to the attack's damage type.

        Args:
            attacker (Self): The creature attacking the target.
            attack (Action): The attack the attacker is using
            consider_distance (bool): Whether to consider the distance between
                this creature and the attacker.

        Returns:
            int: A number representing how valuable the target is.
        """

        if not attack.check_valid_damage(attacker, self):
            return -math.inf

        damage_taken = self.max_hit_points - self.current_hit_points

        weight = damage_taken * self.level
        if consider_distance:
            distance = self.calculate_distance(attacker)
            weight -= distance / 5

        # Only enemies have immunities, resistances, and weaknesses
        if self.team == 2:
            if attack.damage_type in self.immunities:
                weight = -100
            if attack.damage_type in self.resistances.keys():
                weight /= 2
            if attack.damage_type in self.weaknesses.keys():
                weight *= 2

        return weight

    def pick_target(self, attack: Action) -> Self:
        """Picks the best target for the given attack.

        Creates a list of creatures on the opposite side. If there are already
        targets in range, it replaces the list with a list of only targets that
        are in range. If not, it considers all possible targets. For each
        target in the list, it calculates the target's weight, checks if it is
        greater than the currently highest weight seen, and replaces the
        current best target with that target if so. After checking all targets,
        it returns the best target.

        Args:
            attack (Action): The attack being used.

        Returns:
            Self: The most valuable target
        """
        targets = []
        consider_distance = True
        attack_range = attack.range
        targets = (
            self.encounter.enemies
            if self.team == 1
            else self.encounter.players
        )

        targets_in_range = []
        for target in targets:
            if self.calculate_distance(target) <= attack_range:
                targets_in_range.append(target)

        # If we're already in range of targets, only consider them
        if targets_in_range:
            targets = targets_in_range
            consider_distance = False

        best_target = targets[0]
        best_weight = best_target.calculate_weight(
            self, attack, consider_distance
        )

        for target in targets[1:]:
            target_weight = target.calculate_weight(
                self, attack, consider_distance
            )
            if target_weight > best_weight:
                best_target = target
                best_weight = best_target.calculate_weight(
                    self, attack, consider_distance
                )

        return best_target

    def move_to(self, target: Self, action_range: int) -> None:
        """Finds the best route to `target` and moves towards it.

        Repeatedly uses move actions until either `target` is in range or
        move actions are exhausted. Implemented with an outer loop with each
        iteration representing one Stride action and an inner loop with each
        iteration representing one square of movement.

        The outer loop executes as long as the creature has actions remaining.
        It resets the speed per turn and number of diagonal moves taken,
        calculates the distance to `target`, returns if it is in range, and
        takes steps toward `target` until speed runs out if not. Then it
        deducts an action and starts again.

        The inner loop executes as long as `target` is still out of range and
        there is movement speed left to use in this action. It calculates if
        the creature should move diagonally, horizontally, or vertically then
        does so, deducting the amount of speed used then resetting. If the
        creature does not need to move horizontally or vertically, then the
        creature is in range so an action is deducted and the move is complete.

        Args:
            target (Self): The target to move toward
            action_range (int): The range of the action being used
        """
        # Outer loop for each Stride action (move up to speed)
        while self.num_actions > 0:
            speed_remaining = self.speed
            diagonal_moves = 1
            distance = self.calculate_distance(target)

            if distance <= action_range:
                return

            self.log(f"{self} Strides toward {target}, {distance} feet away.")

            # Inner loop for the logic of each individual step (one square)
            while distance > action_range and speed_remaining > 0:
                out_of_range_x = abs(self.position_x - target.position_x) > 1
                out_of_range_y = abs(self.position_y - target.position_y) > 1
                can_travel_diagonally = True
                if diagonal_moves % 2 == 0 and speed_remaining <= 10:
                    can_travel_diagonally = False

                # Both x and y are out of range, step diagonally
                if out_of_range_x and out_of_range_y and can_travel_diagonally:
                    self._step_x(target)
                    self._step_y(target)
                    # Every other diagonal step is five feet of extra movement
                    if diagonal_moves % 2 == 0:
                        speed_remaining -= 5
                    diagonal_moves += 1
                elif out_of_range_x:
                    self._step_x(target)
                elif out_of_range_y:
                    self._step_y(target)
                # In range, done moving
                else:
                    self.num_actions -= 1
                    return
                speed_remaining -= 5

            # At the end of each Stride, reset speed and deduct an action
            self.num_actions -= 1

    def calculate_distance(self, target: Self) -> int:
        """Calculates and returns the distance in feet to `target`.

        Uses math.dist to find the distance to `target` in co-ordinates, then
        multiplies by five to get the distance in feet, and rounds to the
        nearest multiple of five since distance is still considered by each
        5-foot square grid tile.

        Args:
            target (Self): The creature whose distance is being found.

        Returns:
            int: The distance in feet, rounded to five, to `target`.
        """
        base_distance = math.dist(
            [target.position_x, target.position_y],
            [self.position_x, self.position_y],
        )

        distance_in_feet = 5 * base_distance

        rounded_distance = 5 * round(distance_in_feet / 5)

        return rounded_distance

    def take_damage(self, damage: int, damage_type: str) -> None:
        """Subtracts `damage` from the creature's HP.

        `damage` is subtracted from the creature's current hit points,
        and if their hit points fall below 0, the creature dies and is removed
        from the encounter. Also checks to make sure if the damage type is
        vitality, that only undead take damage from it. Although this should
        not happen due to checks elsewhere to prevent vitality attacks from
        targeting non-undead creatures in the first place.

        Args:
            damage (int): The damage the creature is to take.
            damage_type (str): The type of damage being dealt, ex. fire
        """
        self.current_hit_points -= damage

        # Non-undead targets shouldn't be chosen for vitality attacks, but just
        # in case, vitality attacks cannot damage them
        if damage_type == "vitality":
            undead = hasattr(self, "traits") and "undead" in self.traits
            if not undead:
                self.log(f"{self} is not undead, vitality damage invalid")
                return

        if self.current_hit_points <= 0:
            self._die()
        else:
            self.log(f"{self} has {self.current_hit_points} HP remaining!")

    def spell_save(self, damage: int, spell: Spell, attacker: Self) -> None:
        """Performs a basic saving throw against `spell`.

        Checks which saving throw bonus to use, rolls a saving throw against
        the spell DC of the attacker, and calculates the degree of success.
        Depending on the degree of success, the amount of damage is modified
        based on `damage` and the creature takes that amount of damage.

        Args:
            damage (int): The base amount of damage to be taken
            spell (Spell): The spell being saved against
            attacker (Self): The attacker casting the spell

        Raises:
            ValueError: If an invalid save type is passed in.
        """
        save_bonus = 0
        match spell.save:
            case "fortitude":
                save_bonus = self.fortitude
            case "reflex":
                save_bonus = self.reflex
            case "will":
                save_bonus = self.will
            case _:
                raise ValueError(f"Invalid save type: {spell.save}")

        roll = d20.roll()
        saving_throw = roll + save_bonus
        self.log(
            f"{self} rolled a {saving_throw} {spell.save} save against {spell}!"  # noqa: E501
        )

        degree_of_success = calculate_dos(
            roll, saving_throw, attacker.spell_dc
        )

        match degree_of_success:
            case Degree.CRITICAL_SUCCESS:
                self.log(f"{self} critically succeeded. No damage taken!")
                return
            case Degree.SUCCESS:
                damage_taken = math.floor(damage / 2)
                self.log(f"{self} succeeded and takes {damage_taken} damage")
            case Degree.FAILURE:
                damage_taken = damage
                self.log(f"{self} failed and takes {damage_taken} damage")
            case Degree.CRITICAL_FAILURE:
                damage_taken = damage * 2
                self.log(
                    f"{self} critically failed. {damage_taken} damage taken!"
                )

        self.take_damage(damage_taken, spell.damage_type)

    def heal(self, amount: int) -> None:
        """Heals the creature by `amount` hitpoints, up to maximum.

        Args:
            amount (int): The amount of points the creature is healed by.
        """
        self.current_hit_points += amount
        if self.current_hit_points > self.max_hit_points:
            self.current_hit_points = self.max_hit_points

        self.log(f"{self} is now at {self.current_hit_points} hit points!")

    def log(self, message: str) -> None:
        """Adds `message` to the simulation log, or prints it to the console.

        Args:
            message (str): The message to be printed.
        """
        if self.simulation:
            self.simulation.log(message)
        else:
            print(message)

    # Private Methods

    def _roll_initiative(self) -> None:
        # Don't know if a creature is sneaking at the start of the encounter,
        # so assume creatures with higher stealth will typically sneak and
        # roll stealth for initiative
        if self.stealth > self.perception:
            self.initiative = d20.roll() + self.stealth
        else:
            self.initiative = d20.roll() + self.perception

    def _perform_action(self) -> None:
        in_melee = self._check_adjacent_creatures()
        best_action = self.actions[0]
        best_weight = best_action.calculate_weight(
            self.multi_attack, self.num_actions, in_melee, self
        )

        # Just a simple linear search because number of actions should never
        # get too high (typically 3-5, 10-15 at most w/ spells)
        if len(self.actions) > 1:
            for action in self.actions[1:]:
                action_weight = action.calculate_weight(
                    self.multi_attack, self.num_actions, in_melee, self
                )
                if action_weight > best_weight:
                    best_action = action
                    best_weight = best_action.calculate_weight(
                        self.multi_attack, self.num_actions, in_melee, self
                    )

        if isinstance(best_action, Attack):
            target = self.pick_target(best_action)
            if self.calculate_distance(target) > best_action.range:
                self.move_to(target, best_action.range)
                if self.num_actions <= 0:
                    return
            best_action.attack(self, target)
        elif isinstance(best_action, Spell) or isinstance(best_action, Heal):
            best_action.cast(self)
        elif best_action.name.lower() == "raise shield":
            self.log(f"{self} raises their shield!")
            self.armor_class += self.shield_value
            self.shield_raised = True

        self.num_actions -= best_action.cost

    def _check_adjacent_creatures(self):
        opponents = (
            self.encounter.enemies
            if self.team == 1
            else self.encounter.players
        )

        for opponent in opponents:
            if self.calculate_distance(opponent) <= 5:
                return True

        return False

    def _step_x(self, target):
        if self.position_x < target.position_x:
            self.position_x += 1
        else:
            self.position_x -= 1

    def _step_y(self, target):
        if self.position_y < target.position_y:
            self.position_y += 1
        else:
            self.position_y -= 1

    def _die(self) -> None:
        self.log(f"{self} has died!")
        self.is_dead = True
        if self.encounter:
            self.encounter.remove_creature(self)
