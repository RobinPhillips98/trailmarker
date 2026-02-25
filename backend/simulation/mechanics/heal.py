from math import inf

from .actions import Action
from .misc import d8


class Heal(Action):
    def __init__(self, num_heals: int):
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
        most_hurt_ally = self._pick_target(caster)

        if self.slots <= 0 or caster.num_actions < self.cost:
            return -inf

        return self.weight - most_hurt_ally.current_hit_points

    def cast(self, caster) -> None:
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
