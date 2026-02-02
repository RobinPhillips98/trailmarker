from ..creatures.enemy import Enemy
from ..creatures.player import Player
from ..encounters.encounter import Encounter


def run_simulation(
    player_dicts: list[dict[str, any]], enemy_dicts: list[dict[str, any]]
) -> dict[str, str | int | list[str]]:
    """Runs one simulation and returns a dictionary with the data from it.

    Uses the private _Simulation class to keep track of data while the
    simulation runs, then returns a dictionary containing the simulation's
    winner, the number of rounds played, number of players killed, total
    number of players, and a combat log of actions taken during the simulation.


    Args:
        player_dicts (list[dict[str, any]]): Dictionaries to initialize
            Players.
        enemy_dicts (list[dict[str, any]]): Dictionaries to initialize Enemies.

    Returns:
        dict[str, str | int | list[str]]: Dict with data from the simulation.
    """

    # print("Preparing simulation...")
    simulation = _Simulation(player_dicts, enemy_dicts)
    simulation.run()
    # print("Simulation complete!")
    return {
        "winner": simulation.winner,
        "rounds": simulation.rounds,
        "players_killed": simulation.players_killed,
        "total_players": simulation.total_players,
        "log": simulation.sim_log,
    }


class _Simulation:
    def __init__(
        self,
        player_dicts: list[dict[str, any]],
        enemy_dicts: list[dict[str, any]],
    ):
        self.winner: str = ""
        self.players_killed: int = 0
        self.rounds: int = 0
        self.sim_log: list[str] = []

        self.players: list[Player] = []
        self.enemies: list[Enemy] = []
        for player_dict in player_dicts:
            player = Player(player_dict, self)
            self.players.append(player)
        for enemy_dict in enemy_dicts:
            enemy = Enemy(enemy_dict, self)
            self.enemies.append(enemy)

        self.total_players: int = len(self.players)

    def run(self):
        encounter = Encounter(self.players, self.enemies, self)
        self.winner = encounter.run_encounter()

    def log(self, message: str):
        self.sim_log.append(message)
