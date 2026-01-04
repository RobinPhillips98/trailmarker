from .creature import Creature


class Player(Creature):
    def __init__(self, player: dict[any], simulation=None):
        super().__init__(player, simulation)
        self.team = 1
        self.ancestry: str = player["ancestry"]
        self.class_: str = player["class"]

    def die(self) -> None:
        super().die()
        if self.simulation:
            self.simulation.players_killed += 1

    def long_description(self) -> str:
        return f"{self}: Level {self.level} {self.ancestry.capitalize()} {self.class_.capitalize()}"  # noqa
