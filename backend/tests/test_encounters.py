from ..simulation.creatures.enemy import Enemy
from ..simulation.creatures.player import Player
from ..simulation.encounters.encounter import Encounter
from .sample_data import test_enemy, test_player


def test_encounter_initialization():
    player = Player(test_player)
    enemy = Enemy(test_enemy)
    players = [player]
    enemies = [enemy]

    assert player.encounter is None
    assert enemy.encounter is None

    encounter = Encounter(players, enemies)
    # Testing that encounter's lists of creatures filled in correctly
    assert encounter.players[0] == player
    assert encounter.enemies[0] == enemy
    assert player in encounter.creatures and enemy in encounter.creatures
    assert player in encounter.players and player not in encounter.enemies
    assert enemy in encounter.enemies and enemy not in encounter.players

    # Testing that creatures successfully joined encounter
    assert player.encounter == encounter
    assert enemy.encounter == encounter

    # Testing that initiative rolling and sorting was successful
    assert player.initiative == 10 + player.perception
    assert enemy.initiative == 10 + enemy.perception

    assert encounter.creatures[0] == player
    assert encounter.creatures[1] == enemy


def test_run_encounter():
    player = Player(test_player)
    enemy = Enemy(test_enemy)
    players = [player]
    enemies = [enemy]

    encounter = Encounter(players, enemies)

    winner = encounter.run_encounter()
    assert winner == "players"
