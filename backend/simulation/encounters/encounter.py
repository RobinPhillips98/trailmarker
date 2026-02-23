from operator import attrgetter

from ..creatures.creature import Creature
from ..creatures.enemy import Enemy
from ..creatures.player import Player


class Encounter:
    """A single combat encounter typically run by the simulation.

    A combat encounter in which the players and enemies take turns until one
    team is defeated. At which point the encounter ends and returns a string
    telling who won the encounter.

    Attributes:
        players: A list of the Players in the encounter.
        enemies: A list of the Enemies in the encounter.
        creatures: A combined list of all Players and Enemies in the encounter.
        simulation: The simulation running the encounter, if any, primarily
            used for adding to the simulation's combat log.
    """

    # Built-in Methods

    def __init__(
        self, players: list[Player], enemies: list[Enemy], simulation=None
    ):
        """Initializes the encounter with the given players and enemies.

        Sets the player and enemy lists to the given lists, then builds the
        creatures list from them, rolls initiative for each creature, and
        sorts the creature list by initiative.

        Args:
            players (list[Player]): A list of the Players in the encounter.
            enemies (list[Enemy]): A list of the Enemies in the encounter.
            simulation (Simulation, optional): The simulation running the
                encounter. Defaults to None.
        """
        self.players: list[Player] = players
        self.enemies: list[Enemy] = enemies
        self.creatures: list[Creature] = self.players + self.enemies
        self.simulation = simulation
        self.winner = None

        for creature in self.creatures:
            creature.join_encounter(self)

        position_x = 0
        position_y = 0
        if players:
            for player in players:
                player.position_x = position_x
                player.position_y = position_y
                position_y += 1

        if enemies:
            position_x = 10
            position_y = 0
            for enemy in enemies:
                enemy.position_x = position_x
                enemy.position_y = position_y
                position_y += 1

        # Sort by initiative before starting encounter
        self.creatures = sorted(
            self.creatures,
            key=attrgetter("initiative", "team"),  # Enemies win ties
            reverse=True,
        )

    # Public Methods

    def run_encounter(self) -> str:
        """Runs rounds of combat until one side is defeated.

        Returns:
            str: The winner of the encounter.
        """
        self._log("Party:")
        for i in range(len(self.players)):
            self._log(f"{i + 1}. {self.players[i]}")

        self._log("Enemies:")
        for i in range(len(self.enemies)):
            self._log(f"{i + 1}. {self.enemies[i]}")
        self._log()

        self._log("Initiative order: ")
        for i in range(len(self.creatures)):
            creature = self.creatures[i]
            self._log(f"{i + 1}. {creature}: {creature.initiative}")

        rounds = 0
        while not self._check_winner():
            rounds += 1
            self._log(f"Round {rounds}:")
            for creature in self.creatures:
                if not self._check_winner():
                    creature.take_turn()

        self._log(f"{self.winner.capitalize()} won in {rounds} rounds!")
        if self.simulation:
            self.simulation.rounds = rounds

        return self.winner

    def remove_creature(self, creature: Creature) -> None:
        """Removes a creature from the encounter.

        Determines if the creature is a player or enemy, removes it from the
        appropriate list, and then removes it from the overall creatures list.

        Args:
            creature (Creature): The creature to be removed.
        """
        if creature.team == 1:
            self.players.remove(creature)
        elif creature.team == 2:
            self.enemies.remove(creature)

        self.creatures.remove(creature)

    # Private Methods

    def _check_winner(self) -> bool:
        if not self.players:
            self.winner = "enemies"
            return True
        elif not self.enemies:
            self.winner = "players"
            return True
        else:
            return False

    def _log(self, message: str = "") -> None:
        if self.simulation:
            self.simulation.log(message)
        else:
            print(message)
