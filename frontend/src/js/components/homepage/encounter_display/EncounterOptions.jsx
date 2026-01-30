import { useContext, useState } from "react";
import { Button, Input, Space } from "antd";

import api from "../../../api";
import { AuthContext } from "../../../contexts/AuthContext";

/**
 * A component to display options for saving/clearing encounters
 *
 * @param {object} props
 * @param {object} props.enemies The currently selected enemies in the encounter
 * @param {function} props.clearEncounter The function to clear all enemies from the encounter
 * @returns {JSX.Element}
 */
export default function EncounterOptions({ enemies, clearEncounter }) {
  const [encounterName, setEncounterName] = useState("");

  const handleChange = (event) => {
    setEncounterName(event.target.value);
  };

  const { user, token } = useContext(AuthContext);

  /**
   * Saves the given encounter to the database
   *
   * @returns {void}
   */
  async function save() {
    if (enemies.length === 0) {
      alert("Encounter is empty, please add enemies.");
      return;
    }
    const enemy_array = enemies.map((enemy) => ({
      id: enemy.id,
      name: enemy.name,
      quantity: enemy.quantity,
    }));

    const encounter = {
      id: 0,
      name: encounterName,
      enemies: enemy_array,
    };
    try {
      await api.post("/encounters", encounter, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setEncounterName("");
      alert("Encounter saved!");
    } catch (error) {
      alert(error);
    }
  }

  return (
    <div>
      <Button
        style={{ marginRight: 10, marginBottom: 10 }}
        type="primary"
        onClick={save}
        disabled={!user}
      >
        Save Encounter
      </Button>
      <Space.Compact>
        <Input
          type="text"
          id="name"
          placeholder="Enter encounter name..."
          value={encounterName}
          onChange={handleChange}
          disabled={!user}
        />
      </Space.Compact>
      <br />
      <Button
        type="primary"
        danger
        onClick={clearEncounter}
        style={{ marginTop: 10 }}
      >
        Clear Encounter
      </Button>
    </div>
  );
}
