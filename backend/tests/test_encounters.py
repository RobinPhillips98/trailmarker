import pytest

from ..simulation.creatures.enemy import Enemy
from ..simulation.creatures.player import Player
from ..simulation.encounters.encounter import Encounter
from .sample_data import test_enemy, test_player


@pytest.mark.repeat(25)
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
    assert player.initiative > 0
    assert enemy.initiative > 0

    if player.initiative > enemy.initiative:
        assert (
            encounter.creatures[0] == player
            and encounter.creatures[1] == enemy
        ), "Player wins initiative failed"
    elif enemy.initiative > player.initiative:
        assert (
            encounter.creatures[0] == enemy
            and encounter.creatures[1] == player
        ), "Enemy wins initiative failed"
    elif player.initiative == enemy.initiative:
        assert (
            encounter.creatures[0] == enemy
            and encounter.creatures[1] == player
        ), "Initiative tie breaker failed"


@pytest.mark.repeat(25)
def test_run_encounter():
    player = Player(test_player)
    enemy = Enemy(test_enemy)
    players = [player]
    enemies = [enemy]

    encounter = Encounter(players, enemies)

    winner = encounter.run_encounter()
    assert winner == "players"
