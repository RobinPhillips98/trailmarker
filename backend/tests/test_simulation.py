from ..simulation.core.simulation import run_simulation
from .sample_data import test_enemies, test_party


def test_sim_players_win():
    enemies = test_enemies
    players = test_party

    print()  # for neatness in viewing output
    sim_results = run_simulation(players, enemies)
    winner = sim_results["winner"]
    log = sim_results["log"]
    assert log
    print("Log:")
    for message in log:
        print(message)
    assert winner == "players"


def test_sim_enemies_win():
    enemies = test_enemies + test_enemies + test_enemies
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
