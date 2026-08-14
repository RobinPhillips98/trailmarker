from tests.failures import sync_failure

SIMULATION_ROUTE = "/simulation/"


def _get_enemy_ids(client, count=2):
    response = client.get("/enemies/")
    assert response.status_code == 200

    enemies = response.json()
    assert len(enemies) >= count

    selected = enemies[:count]
    return [
        {"id": enemy["id"], "quantity": 2 if index == 0 else 1}
        for index, enemy in enumerate(selected)
    ]


def test_run_simulation(auth_client, character_factory):
    character_factory(template="fighter")
    character_factory(template="cleric")
    character_factory(template="rogue")
    character_factory(template="wizard")

    request = {"enemies": _get_enemy_ids(auth_client)}

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


def test_run_simulation_with_invalid_enemy(auth_client, character_factory):
    character_factory(template="fighter")
    character_factory(template="cleric")

    enemy_list = [
        {"id": 999, "quantity": 1},  # Invalid enemy ID
    ]

    request = {"enemies": enemy_list}

    response = auth_client.post(SIMULATION_ROUTE, json=request)

    assert response.status_code == 404
    assert "Enemy with ID 999 not found" in response.json()["detail"]


def test_run_simulation_internal_server_error(
    auth_client, character_factory, monkeypatch
):
    character_factory(template="fighter")
    character_factory(template="cleric")

    # enemy_list = [
    #     {"id": 1, "quantity": 1},
    # ]

    request = {"enemies": _get_enemy_ids(auth_client)}

    # Patch the run_simulation function to raise an exception
    monkeypatch.setattr("api.routes.simulation.run_simulation", sync_failure)

    response = auth_client.post(SIMULATION_ROUTE, json=request)

    assert response.status_code == 500
    assert response.json()["detail"] == "Internal Server Error"
