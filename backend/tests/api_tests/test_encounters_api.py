ENCOUNTERS_ROUTE = "/encounters/"


def test_read_encounters_list(auth_client, encounter_factory):
    for i in range(4):
        encounter_factory()
    response = auth_client.get(ENCOUNTERS_ROUTE)
    assert response.status_code == 200
    encounter_list = response.json()
    assert len(encounter_list) == 4
    for encounter in encounter_list:
        assert "id" in encounter.keys()
        assert "name" in encounter.keys()
        assert encounter["enemies"] == [{"id": 1, "quantity": 2}]


def test_read_encounter(auth_client, created_encounter):
    encounter_id = created_encounter["id"]
    response = auth_client.get(f"{ENCOUNTERS_ROUTE}{encounter_id}")
    assert response.status_code == 200
    returned_encounter = response.json()

    assert returned_encounter["id"] == encounter_id
    assert returned_encounter["name"] == created_encounter["name"]
    assert returned_encounter["enemies"] == created_encounter["enemies"]


def test_create_encounter(shared_auth_client, encounter_payload):
    response = shared_auth_client.post(
        ENCOUNTERS_ROUTE, json=encounter_payload
    )
    assert response.status_code == 201

    returned_encounter = response.json()

    assert "id" in returned_encounter.keys()
    assert returned_encounter["name"] == encounter_payload["name"]
    assert returned_encounter["enemies"] == encounter_payload["enemies"]


def test_update_encounter(auth_client, created_encounter):
    encounter_id = created_encounter["id"]
    request = {
        "name": f"{created_encounter["name"]}_updated",
        "enemies": [{"id": 1, "quantity": 2}, {"id": 2, "quantity": 1}],
    }
    response = auth_client.patch(
        f"{ENCOUNTERS_ROUTE}{encounter_id}", json=request
    )
    assert response.status_code == 200
    returned_encounter = response.json()

    assert returned_encounter["id"] == created_encounter["id"]
    assert returned_encounter["name"] == f"{created_encounter["name"]}_updated"
    assert returned_encounter["enemies"] == [
        {"id": 1, "quantity": 2},
        {"id": 2, "quantity": 1},
    ]


def test_delete_encounter(shared_auth_client, encounter_payload):
    creation_response = shared_auth_client.post(
        ENCOUNTERS_ROUTE, json=encounter_payload
    )
    created_encounter = creation_response.json()
    encounter_id = created_encounter["id"]
    response = shared_auth_client.delete(f"{ENCOUNTERS_ROUTE}{encounter_id}")
    assert response.status_code == 200

    response = shared_auth_client.get(f"{ENCOUNTERS_ROUTE}{encounter_id}")
    assert response.status_code == 404
