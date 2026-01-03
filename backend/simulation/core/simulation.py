from ..creatures.enemy import Enemy
from ..creatures.player import Player
from ..encounters.encounter import Encounter


class _Simulation:
    def __init__(
        self, player_dicts: list[dict[any]], enemy_dicts: list[dict[any]]
    ):
        self.winner: str = ""
        self.sim_log: list[str] = []
        self.players: list[Player] = []
        self.enemies: list[Enemy] = []

        for player_dict in player_dicts:
            player = Player(player_dict, self)
            self.players.append(player)
        for enemy_dict in enemy_dicts:
            enemy = Enemy(enemy_dict, self)
            self.enemies.append(enemy)

    def run(self):
        encounter = Encounter(self.players, self.enemies, self)
        self.winner = encounter.run_encounter()

    def log(self, message: str):
        self.sim_log.append(message)


def run_simulation(player_dicts: list[any], enemy_dicts: list[any]) -> str:
    print("Preparing simulation...")
    simulation = _Simulation(player_dicts, enemy_dicts)
    simulation.run()
    print("Simulation complete!")
    return {"winner": simulation.winner, "log": simulation.sim_log}
