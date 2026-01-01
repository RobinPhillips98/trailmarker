from .creature import Creature


class Player(Creature):
    def __init__(self, player: dict[any]):
        super().__init__(player)
        self.team = 1
        self.ancestry: str = player["ancestry"]
        self.class_: str = player["class"]

    def long_description(self) -> str:
        return f"{self}: Level {self.level} {self.ancestry.capitalize()} {self.class_.capitalize()}"  # noqa
