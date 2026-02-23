import math
import random
from typing import Self

from ..mechanics.actions import Action, Attack, Spell
from ..mechanics.misc import Degree, Die, d20


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
                spell = Spell(spell_dict)
                self.spells.append(spell)
        except KeyError:
            self.spells = None

        self.actions: list[Action] = []
        if self.attacks:
            self.actions.extend(self.attacks)
        if self.spells:
            self.actions.extend(self.spells)

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
        self.position_x: int = None
        self.position_y: int = None

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

        self._log(f"{self}'s turn:")
        self.num_actions = 3
        self.map = 0

        # Simulating one action spent on movement
        self.num_actions -= 1
        # TODO: Proper movement (stretch goal)

        while self.num_actions > 0:
            if self.encounter.players and self.encounter.enemies:
                self._perform_action()
            else:
                break

    def calculate_weight(self) -> int:
        """Calculates how valuable a target the creature is.

        Returns:
            int: A number representing how valuable the target is.
        """
        weight = (self.max_hit_points - self.current_hit_points) * self.level

        return weight

    def take_damage(self, damage: int) -> None:
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
            self._log(f"{self} has {self.current_hit_points} HP remaining!")

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
        best_action = self.actions[0]
        best_weight = best_action.calculate_weight(self.map)

        # Just a simple linear search because number of actions should never
        # get too high (typically 3-5, 10-15 at most w/ spells)
        for action in self.actions[1:]:
            if action.calculate_weight(self.map) > best_weight:
                best_action = action
                best_weight = best_action.calculate_weight(self.map)

        if isinstance(best_action, Attack):
            target = self._pick_target()
            self._attack(best_action, target)
        elif isinstance(best_action, Spell):
            self._cast_spell(best_action)

        self.num_actions -= best_action.cost

    def _pick_target(self) -> Self:
        targets = []
        if self.team == 1:
            targets = self.encounter.enemies
        elif self.team == 2:
            targets = self.encounter.players

        best_target = targets[0]
        best_weight = best_target.calculate_weight()

        for target in targets[1:]:
            if target.calculate_weight() > best_weight:
                best_target = target
                best_weight = best_target.calculate_weight()

        return best_target

    def _attack(self, attack: Action, target: Self) -> bool:
        self._log(f"{self} is attacking {target} with their {attack}.")

        # Calculate attack roll and check for hit before calculating damage
        attack_roll = d20.roll()
        if isinstance(attack, Attack):
            attack_total = attack_roll + attack.attack_bonus - self.map
            if self.encounter:
                self.map += 5
        elif isinstance(attack, Spell):
            attack_total = attack_roll + self.spell_attack_bonus
        self._log(f"{self} rolled {attack_total} to attack.")

        if attack_roll == 20 or attack_total >= target.armor_class + 10:
            critical_hit = True
        else:
            critical_hit = False

        if attack_total < target.armor_class:
            # Rolling a 20 upgrades a miss into a non-critical hit, so set
            # critical_hit back to false and proceed with damage
            if attack_roll == 20:
                critical_hit = False
            # If we didn't hit the target AC and we didn't roll a 20,
            # we don't do damage, so return
            else:
                self._log("Miss!")
                return False

        self._log("Hit!")

        damage_type = attack.damage_type
        damage_die = Die(attack.die_size)

        damage_roll = damage_die.roll()
        damage = (attack.num_dice * damage_roll) + attack.damage_bonus
        if critical_hit:
            self._log(f"{self} dealt a critical hit to {target}!")
            damage *= 2

        self._log(f"{self} dealt {damage} {damage_type} damage to {target}!")
        target.take_damage(damage)

        return True

    def _cast_spell(self, spell: Spell) -> None:
        self._log(f"{self} is casting {spell}!")

        if spell.targets:
            for i in range(spell.targets):
                target = self._pick_target()
                self._attack(spell, target)
        elif spell.area_size:
            self._aoe_spell(spell)

        if spell.level >= 1:
            spell.slots -= 1

    def _aoe_spell(self, spell: Spell):
        num_targets = 0
        match spell.area_type:
            case "burst":
                num_targets = math.ceil(spell.area_size / 5)
            case "cone":
                num_targets = math.ceil(spell.area_size / 10)
            case "emanation":
                num_targets = math.ceil(spell.area_size / 5)
            case "line":
                num_targets = math.ceil(spell.area_size / 30)
            case _:
                raise Exception("Invalid spell area type")

        if self.team == 1:
            enemies = self.encounter.enemies
            if num_targets <= len(enemies):
                targets = random.sample(enemies, num_targets)
            else:
                targets = enemies
        elif self.team == 2:
            players = self.encounter.players
            if num_targets <= len(players):
                targets = random.sample(players, num_targets)
            else:
                targets = players

        # TODO: Add support for various damage type effects
        damage_die = Die(spell.die_size)

        damage_roll = damage_die.roll()
        damage = (spell.num_dice * damage_roll) + spell.damage_bonus

        target_names = ", ".join(map(str, targets))
        self._log(f"{self} is attacking {target_names} with {spell}!")
        for target in targets:
            target._spell_save(damage, spell, self)

    def _spell_save(self, damage: int, spell: Spell, attacker: Self) -> None:
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
        self._log(
            f"{self} rolled a {saving_throw} {spell.save} saving throw against {spell}!"  # noqa
        )

        difficulty = attacker.spell_dc
        if saving_throw >= difficulty + 10:
            degree_of_success = Degree.CRITICAL_SUCCESS
        elif saving_throw >= difficulty:
            degree_of_success = Degree.SUCCESS
        elif saving_throw <= difficulty - 10:
            degree_of_success = Degree.CRITICAL_FAILURE
        else:
            degree_of_success = Degree.FAILURE

        if roll == 20 and degree_of_success < Degree.CRITICAL_SUCCESS:
            degree_of_success += 1
        elif roll == 1 and degree_of_success > Degree.CRITICAL_FAILURE:
            degree_of_success -= 1

        match degree_of_success:
            case Degree.CRITICAL_SUCCESS:
                damage_taken = 0
                self._log(f"{self} critically succeeded. No damage taken!")
            case Degree.SUCCESS:
                damage_taken = math.floor(damage / 2)
                self._log(f"{self} succeeded and takes {damage_taken} damage")
            case Degree.FAILURE:
                damage_taken = damage
                self._log(f"{self} failed and takes {damage_taken} damage")
            case Degree.CRITICAL_FAILURE:
                damage_taken = math.floor(damage * 2)
                self._log(
                    f"{self} critically failed. {damage_taken} damage taken!"
                )

    def _die(self) -> None:
        self._log(f"{self} has died!")
        self.is_dead = True
        if self.encounter:
            self.encounter.remove_creature(self)

    def _log(self, message: str) -> None:
        if self.simulation:
            self.simulation.log(message)
        else:
            print(message)
