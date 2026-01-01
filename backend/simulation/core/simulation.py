from ..creatures.enemy import Enemy
from ..creatures.player import Player
from ..encounters.encounter import Encounter


def run_simulation(player_dicts: list[any], enemy_dicts: list[any]) -> str:
    print("Preparing simulation...")
    players, enemies = initialize_creatures(player_dicts, enemy_dicts)
    encounter = Encounter(players, enemies)
    winner = encounter.run_encounter()
    print("Simulation complete!")
    return winner


def initialize_creatures(
    player_dicts: list[any], enemy_dicts: list[any]
) -> list[list[Player] | list[Enemy]]:
    players = []
    enemies = []

    for player_dict in player_dicts:
        player = Player(player_dict)
        players.append(player)
    for enemy_dict in enemy_dicts:
        enemy = Enemy(enemy_dict)
        enemies.append(enemy)

    return [players, enemies]
