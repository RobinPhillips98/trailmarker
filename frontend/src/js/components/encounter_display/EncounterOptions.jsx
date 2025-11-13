import api from "../../api";
import { useState } from "react";
import { Button, Input, Space } from "antd";

function EncounterOptions(props) {
  const [encounterName, setEncounterName] = useState("");

  const handleChange = (event) => {
    setEncounterName(event.target.value);
  };

  async function save() {
    if (props.enemies.length === 0) {
      alert("Encounter is empty, please add enemies.")
      return;
    }
    const enemy_array = props.enemies.map((enemy) => ({
      id: enemy.id,
      name: enemy.name,
      quantity: enemy.quantity,
    }));

    const encounter = {
      id: 0,
      name: encounterName,
      enemies: enemy_array,
    };

    await api.post("/encounters", encounter);
    setEncounterName("");
  }

  return (
    <div >
      <Button style={{marginRight: 10, marginBottom: 10}} type="primary" onClick={save}>
        Save Encounter
      </Button>
      <Space.Compact>
        <Input
          type="text"
          id="name"
          placeholder="Enter encounter name..."
          value={encounterName}
          onChange={handleChange}
        />
      </Space.Compact>
      <br />
      <Button danger onClick={props.clearEncounter}>Clear Encounter</Button>
    </div>
  );
}

export default EncounterOptions;
