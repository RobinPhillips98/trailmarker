from .creature import Creature


class Player(Creature):
    def __init__(self, player: dict[any]):
        super().__init__(player)
        self.team = 1