from .creature import Creature


class Player(Creature):
    """A character belong to one of the players in the user's party.

    Attributes:
        ancestry: The character's ancestry, ex. elf or human
        class_: The character's class, ex. fighter or wizard
    """

    # Built-in Methods

    def __init__(self, player: dict[any], simulation=None):
        """Initializes the player based on the passed in dictionary.

        Args:
            player (dict[any]): The data used to build the player
            simulation (Simulation, optional): The simulation the creature is
                in. Defaults to None.
        """
        super().__init__(player, simulation)
        self.team = 1
        self.ancestry: str = player["ancestry"]
        self.class_: str = player["class"]

    # Public Methods

    def long_description(self) -> str:
        """Gives a well-formatted description of the player.

        Returns:
            str: The long description of the player.
        """
        return f"{self}: Level {self.level} {self.ancestry.capitalize()} {self.class_.capitalize()}"  # noqa

    # Private Methods

    def _die(self) -> None:
        super()._die()
        if self.simulation:
            self.simulation.players_killed += 1
