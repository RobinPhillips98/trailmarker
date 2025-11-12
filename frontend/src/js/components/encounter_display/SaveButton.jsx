import api from "../../api";
import { useState } from "react";

function SaveButton(props) {
  const [encounterName, setEncounterName] = useState("");

  const handleChange = (event) => {
    setEncounterName(event.target.value);
  };

  async function save() {
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
    <div>
      <button onClick={save}>Save Encounter</button>
      <input
        type="text"
        id="name"
        placeholder="Enter encounter name..."
        value={encounterName}
        onChange={handleChange}
      />
      <button onClick={props.clearEncounter}>Clear Encounter</button>
    </div>
  );
}

export default SaveButton;
