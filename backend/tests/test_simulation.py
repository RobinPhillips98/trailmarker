import pytest

from ..simulation.core.simulation import run_simulation
from .sample_data import test_enemies, test_party

total_sims = 100


@pytest.mark.repeat(total_sims / 2)
def test_sim_players_win():
    enemies = test_enemies
    players = test_party + test_party

    print()  # for neatness in viewing output
    sim_results = run_simulation(players, enemies)
    winner = sim_results["winner"]
    log = sim_results["log"]
    assert log
    print("Log:")
    for message in log:
        print(message)
    assert winner == "players"


@pytest.mark.repeat(total_sims / 2)
def test_sim_enemies_win():
    # Ensuring there are far too many enemies for the players to ever win
    enemies = (
        test_enemies
        + test_enemies
        + test_enemies
        + test_enemies
        + test_enemies
    )
    players = test_party

    print()
    sim_results = run_simulation(players, enemies)
    winner = sim_results["winner"]
    log = sim_results["log"]
    assert log
    print("Log:")
    for message in log:
        print(message)
    assert winner == "enemies"
