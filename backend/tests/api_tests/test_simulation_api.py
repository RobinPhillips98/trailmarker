SIMULATION_ROUTE = "/simulation/"


def test_run_simulation(auth_client, character_factory):
    character_factory(template="fighter")
    character_factory(template="cleric")
    character_factory(template="rogue")
    character_factory(template="wizard")

    enemy_list = [
        {"id": 1, "quantity": 2},
        {"id": 2, "quantity": 1},
    ]

    request = {"enemies": enemy_list}

    response = auth_client.post(SIMULATION_ROUTE, json=request)

    assert response.status_code == 200

    sim_response = response.json()

    total_sims = sim_response["total_sims"]
    assert total_sims == 100
    assert sim_response["wins"] >= 0
    assert (
        sim_response["wins_ratio"] == sim_response["wins"] / total_sims * 100
    )

    deaths = sum(data["players_killed"] for data in sim_response["sim_data"])
    assert sim_response["average_deaths"] == deaths / total_sims

    total_rounds = sum(data["rounds"] for data in sim_response["sim_data"])
    assert sim_response["average_rounds"] == total_rounds / total_sims
