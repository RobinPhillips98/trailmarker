import math
from typing import Self

from ..mechanics.actions import Action, Attack, Spell
from ..mechanics.heal import Heal
from ..mechanics.misc import Degree, calculate_dos, d20


class Creature:
    """A creature, such as a player or enemy, ready for use in an encounter.

    A representation of a creature from Pathfinder 2E with support for basic
    stats, attribute modifiers, skills, saving throws as well as methods
    for taking turns, attacking, and taking damage. For sake of brevity,
    only non-obvious attributes will be explained.

    Attributes:
        attacks: A list of Attack objects representing the creature's weapon
            attacks.
        actions: A list of the creature's actions, including attacks.
        encounter: The encounter the creature is in, if any, primarily used
            for removing the creature from the encounter on death.
        initiative: The creature's initiative, calculated at the beginning of
            an encounter, used to decide the order that creatures take turns.
        num_actions: The number of actions the creature has, set to 3 at the
            beginning of the creature's turn. Turn ends at 0 actions.
        map: The creature's current multiple attack penalty, increases each
            time the creature attacks in a turn to make multiple attacks in
            one turn less likely to hit
        team: 1 if the creature is a player, 2 if the creature is an enemy.
        simulation: The simulation the creature is in, if any, primarily used
            for adding to the simulation's combat log.
    """

    # Built-in Methods

    def __init__(self, creature: dict[str, any], simulation=None):
        """Initializes the creature based on the given dictioanry

        Args:
            creature (dict[str, any]): Data used to build the Creature.
            simulation (Simulation, optional): The simulation the creature is
                in. Defaults to None.
        """
        # Basic Stats
        self.name: str = creature["name"]
        self.level: int = creature["level"]
        self.perception: int = creature["perception"]
        self.max_hit_points: int = creature["max_hit_points"]
        self.current_hit_points: int = self.max_hit_points
        self.speed: int = creature["speed"]
        self.armor_class: int = creature["defenses"]["armor_class"]
        self.spell_attack_bonus: int = creature.get("spell_attack_bonus")
        self.spell_dc: int = creature.get("spell_dc")

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

        self.spells: list[Spell] = []
        try:
            for spell_dict in creature["actions"]["spells"]:
                spell = Spell(spell_dict, self.spell_attack_bonus)
                self.spells.append(spell)
        except KeyError:
            self.spells = None

        try:
            self.heals: int = creature["actions"].get("heals")
        except KeyError:
            self.heals: int = None

        self.actions: list[Action] = []
        if self.attacks:
            self.actions.extend(self.attacks)
        if self.spells:
            self.actions.extend(self.spells)
        if self.heals:
            heal = Heal(self.heals)
            self.actions.append(heal)

        # Encounter Data
        self.encounter = None
        self.initiative: int = 0
        self.num_actions: int = 0
        self.map: int = 0
        self.team: int = 0
        self.is_dead: bool = False

        # Simulation Data
        self.simulation = simulation

        # Map Data
        self.position_x: int = 0
        self.position_y: int = 0

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
        """The creature picks an action and performs that action.

        The creature selects its action with the highest weight. If that action
        is an attack, the creature selects a target and attacks that target.
        """
        if not self.encounter:
            raise Exception("Turns cannot be taken outside of an encounter")

        self.log(f"{self}'s turn:")
        self.log(f"{self}'s current hit points: {self.current_hit_points}")
        self.num_actions = 3
        self.map = 0

        while self.num_actions > 0:
            if self.encounter.players and self.encounter.enemies:
                self._perform_action()
            else:
                break

    def calculate_weight(self, attacker: Self, consider_distance: bool) -> int:
        """Calculates how valuable a target the creature is.

        Returns:
            int: A number representing how valuable the target is.
        """
        damage_taken = self.max_hit_points - self.current_hit_points

        weight = damage_taken * self.level
        if consider_distance:
            distance = self.calculate_distance(attacker)
            weight -= distance / 5

        return weight

    def pick_target(self, attack_range) -> Self:
        targets = []
        consider_distance = True
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
        best_weight = best_target.calculate_weight(self, consider_distance)

        for target in targets[1:]:
            if target.calculate_weight(self, consider_distance) > best_weight:
                best_target = target
                best_weight = best_target.calculate_weight(
                    self, consider_distance
                )

        return best_target

    def move_to(self, target: Self, attack_range: int) -> None:
        speed_remaining = self.speed

        # Outer loop for each Stride action (move up to speed)
        while self.num_actions >= 0:
            diagonal_moves = 1
            distance = self.calculate_distance(target)

            if distance <= attack_range:
                return

            self.log(f"{self} Strides toward {target}, {distance} feet away.")

            # Inner loop for the logic of each individual step (one square)
            while distance > attack_range and speed_remaining > 0:
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

            speed_remaining = self.speed
            self.num_actions -= 1

    def calculate_distance(self, target: Self) -> int:
        base_distance = math.dist(
            [target.position_x, target.position_y],
            [self.position_x, self.position_y],
        )

        # We have the distance in squares, but we want it in feet
        distance_in_feet = 5 * base_distance

        # Then round to the nearest multiple of five to account for needing to
        # measure distance in 5-foot squares
        rounded_distance = 5 * round(distance_in_feet / 5)

        return rounded_distance

    def take_damage(self, damage: int, damage_type: str) -> None:
        """Subtracts the given damage from the creature's HP.

        The given damage is subtracted from the creature's current hit points,
        and if their hit points fall below 0, the creature dies and is removed
        from the encounter.

        Args:
            damage (int): The damage the creature is to take.
        """
        self.current_hit_points -= damage

        if self.current_hit_points <= 0:
            self._die()
        else:
            self.log(f"{self} has {self.current_hit_points} HP remaining!")

    def spell_save(self, damage: int, spell: Spell, attacker: Self) -> None:
        save_bonus = 0
        match spell.save:
            case "fortitude":
                save_bonus = self.fortitude
            case "reflex":
                save_bonus = self.reflex
            case "will":
                save_bonus = self.will
            case _:
                raise Exception("Invalid save type")

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
                damage_taken = 0
                self.log(f"{self} critically succeeded. No damage taken!")
            case Degree.SUCCESS:
                damage_taken = math.floor(damage / 2)
                self.log(f"{self} succeeded and takes {damage_taken} damage")
            case Degree.FAILURE:
                damage_taken = damage
                self.log(f"{self} failed and takes {damage_taken} damage")
            case Degree.CRITICAL_FAILURE:
                damage_taken = math.floor(damage * 2)
                self.log(
                    f"{self} critically failed. {damage_taken} damage taken!"
                )

        self.take_damage(damage_taken, spell.damage_type)

    def heal(self, amount: int) -> None:
        self.current_hit_points += amount
        if self.current_hit_points > self.max_hit_points:
            self.current_hit_points = self.max_hit_points

        self.log(f"{self} is now at {self.current_hit_points} hit points!")

    def log(self, message: str) -> None:
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
            self.map, self.num_actions, in_melee, self
        )

        # Just a simple linear search because number of actions should never
        # get too high (typically 3-5, 10-15 at most w/ spells)
        for action in self.actions[1:]:
            action_weight = action.calculate_weight(
                self.map, self.num_actions, in_melee, self
            )
            if action_weight > best_weight:
                best_action = action
                best_weight = best_action.calculate_weight(
                    self.map, self.num_actions, in_melee, self
                )

        if isinstance(best_action, Attack):
            target = self.pick_target(best_action.range)
            if self.calculate_distance(target) > best_action.range:
                self.move_to(target, best_action.range)
                if self.num_actions <= 0:
                    return
            best_action.attack(self, target)
        elif isinstance(best_action, Spell) or isinstance(best_action, Heal):
            best_action.cast(self)

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
