"""Defines the Heal subclass extending Action, and its methods."""

from math import inf

from .actions import Action
from .misc import d8


class Heal(Action):
    """A representation of a Heal spell.

    Attributes:
        name: The name of the action
        slots: The number of heal spells prepared
        cost: An integer indicating the cost of the action from 1 to 3
        weight: An integer indicating how likely the action is to be selected
        traits: The list of traits the action has, ex. agile or finesse
        range: The distance at which the action can target a creature
        ranged: Whether the action can be used at a distance
        bonus: The bonus added to the amount of hit points healed
    """

    def __init__(self, num_heals: int):
        """Initializes a Heal action with `num_heals` number of slots prepared.

        Args:
            num_heals (int): The number of slots prepared for Heal spells.
        """
        self.name: str = "Heal"
        self.slots: int = num_heals
        self.cost: int = 2
        self.weight: int = 25
        self.range: int = 30
        self.ranged: bool = True
        self.bonus: int = 8

    def calculate_weight(
        self,
        penalty: int,
        actions_remaining: int,
        in_melee: bool = False,
        caster=None,
    ) -> int:
        """Calculates how valuable the Heal is to perform.

        First checks if the caster is able to cast the Heal action. If not,
        returns `-inf`. Otherwise, finds the most hurt ally in the caster's
        party and returns the difference between `self.weight` and that ally's
        current hit points.

        Args:
            penalty (int): Taken from parent, unused in the Heal action.
            actions_remaining (int): Taken from parent, unused in the Heal
                action.
            in_melee (bool, optional): Taken from parent, unused in the Heal
                action.
            caster (Creature, optional): The creature casting the heal spell.
                Defaults to None.

        Returns:
            int: The value of the heal, or -inf if the heal cannot be
                performed.
        """
        if self.slots <= 0 or caster.num_actions < self.cost:
            return -inf

        most_hurt_ally = self._pick_target(caster)

        return self.weight - most_hurt_ally.current_hit_points

    def cast(self, caster) -> None:
        """Casts the heal spell on the ally who needs it most.

        Picks the most wounded ally, rolls a die to decide the number of points
        healed, and heals the ally for that number of points.

        Args:
            caster (Creature): The creature casting the Heal spell
        """
        target = self._pick_target(caster)
        if caster.calculate_distance(target) > self.range:
            caster.move_to(target, self.range)

        heal_roll = d8.roll()
        total_healing = heal_roll + self.bonus
        caster.log(
            f"{caster} cast Heal on {target} for {total_healing} hit points ({heal_roll} + {self.bonus})"  # noqa: E501
        )
        target.heal(total_healing)

        self.slots -= 1
        if self.slots <= 0:
            caster.actions.remove(self)

    def _pick_target(self, caster):
        allies = (
            caster.encounter.players
            if caster.team == 1
            else caster.encounter.enemies
        )

        most_hurt_ally = allies[0]

        for ally in allies[1:]:
            if ally.current_hit_points < most_hurt_ally.current_hit_points:
                most_hurt_ally = ally

        return most_hurt_ally
