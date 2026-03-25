"""Defines core simulation driver function and private Simulation class."""

from typing import Any

from ..creatures.enemy import Enemy
from ..creatures.player import Player
from ..encounters.encounter import Encounter


def run_simulation(
    player_dicts: list[dict[str, Any]],
    enemy_dicts: list[dict[str, Any]],
    parameters: dict[str, int] = {
        "starting_distance": 50,
        "health_multiplier": 1.0,
    },
) -> dict[str, str | int | list[str]]:
    """Runs one simulation and returns a dictionary with the data from it.

    Uses the private _Simulation class to keep track of data while the
    simulation runs, then returns a dictionary containing the simulation's
    winner, the number of rounds played, number of players killed, total
    number of players, and a combat log of actions taken during the simulation.

    Args:
        player_dicts (list[dict[str, Any]]): Dictionaries to initialize
            Players.
        enemy_dicts (list[dict[str, Any]]): Dictionaries to initialize Enemies.
        parameters: Dictionary with various settings for fine-tuning the
            simulation, such as starting distance and player health multiplier.

    Returns:
        dict[str, str | int | list[str]]: Dict with data from the simulation.
    """

    simulation = _Simulation(player_dicts, enemy_dicts, parameters)
    simulation.run()
    return {
        "winner": simulation.winner,
        "rounds": simulation.rounds,
        "players_killed": simulation.players_killed,
        "total_players": simulation.total_players,
        "log": simulation.sim_log,
    }


class _Simulation:
    """A private class used to drive a single run of a simulation.

    Attributes:
        winner: The winner of the simulation.
        players_killed: The number of players killed in the simulation.
        rounds: The number of rounds the simulation lasted.
        starting_distance: The distance between the players and enemies at the
            start of the simulation.
        sim_log: A list of messages to be displayed by the frontend, showing
            a play-by-play description of the actions taken in the simulation.
        players: The Player objects used in the simulation.
        enemies: The enemy objects used in the simulation.
        total_players: The total number of players in the simulation.
    """

    def __init__(
        self,
        player_dicts: list[dict[str, Any]],
        enemy_dicts: list[dict[str, Any]],
        parameters: dict[str, int],
    ):
        self.winner: str = ""
        self.players_killed: int = 0
        self.rounds: int = 0
        self.starting_distance = parameters["starting_distance"]
        self.sim_log: list[str] = []

        self.players: list[Player] = []
        self.enemies: list[Enemy] = []
        for player_dict in player_dicts:
            player = Player(player_dict, self, parameters["health_multiplier"])
            self.players.append(player)
        for enemy_dict in enemy_dicts:
            enemy = Enemy(enemy_dict, self)
            self.enemies.append(enemy)

        self.total_players: int = len(self.players)

    def run(self):
        """Runs one encounter, setting `self.winner` based on the results."""
        encounter = Encounter(
            self.players, self.enemies, self, self.starting_distance
        )
        self.winner = encounter.run_encounter()

    def log(self, message: str):
        """Appends `message` to `sim_log`. To be displayed by the frontend.

        Args:
            message (str): The message to be appended.
        """
        self.sim_log.append(message)
