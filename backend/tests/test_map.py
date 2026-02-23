from ..simulation.creatures.enemy import Enemy
from ..simulation.creatures.player import Player
from ..simulation.mechanics.map import GridMap
from .sample_data import test_enemies, test_party


def test_empty_map():
    grid_map = GridMap()
    for row in grid_map.grid:
        assert not all(row)


def test_map_with_creatures():
    players = [Player(player) for player in test_party]
    enemies = [Enemy(enemy) for enemy in test_enemies]

    grid_map = GridMap(players, enemies)
    for i in range(len(players)):
        assert grid_map.grid[i][0] == players[i]
        assert players[i].position_x == 0
        assert players[i].position_y == i

    for i in range(len(enemies)):
        assert grid_map.grid[i][10] == enemies[i]
        assert enemies[i].position_x == 10
        assert enemies[i].position_y == i
