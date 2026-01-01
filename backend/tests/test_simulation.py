from ..simulation.core.simulation import run_simulation
from .sample_data import test_enemies, test_party


def test_sim_players_win():
    enemies = test_enemies
    players = test_party

    print()  # for neatness in viewing output
    winner = run_simulation(players, enemies)
    assert winner == "players"


def test_sim_enemies_win():
    enemies = test_enemies + test_enemies + test_enemies
    players = test_party

    print()
    winner = run_simulation(players, enemies)
    assert winner == "enemies"
