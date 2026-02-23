from ..creatures.creature import Creature
from ..creatures.enemy import Enemy
from ..creatures.player import Player


class GridMap:
    def __init__(
        self, players: list[Player] = None, enemies: list[Enemy] = None
    ):
        # Each square is 5 feet, so this creates a 100 x 200 ft. grid
        rows, cols = 20, 40
        self.grid: list[list[Creature]] = [
            [None for _ in range(cols)] for _ in range(rows)
        ]

        position_x = 0
        position_y = 0
        if players:
            for player in players:
                if position_y >= rows:
                    position_x += 1
                    position_y = 0
                self.grid[position_y][position_x] = player
                player.position_x = position_x
                player.position_y = position_y
                position_y += 1

        if enemies:
            position_x += 10
            position_y = 0
            for enemy in enemies:
                if position_y >= rows:
                    position_x += 1
                    position_y = 0
                self.grid[position_y][position_x] = enemy
                enemy.position_x = position_x
                enemy.position_y = position_y
                position_y += 1
