import { useContext, useState } from "react";
import { Button, Input, Space, Row, Col } from "antd";

import api from "../../../api";
import { AuthContext } from "../../../contexts/AuthContext";
import SavedEncounters from "./saved_encounters/SavedEncounters";

/**
 * A component to display controls for saving, loading, and clearing encounters
 *
 * @param {object} props
 * @param {object} props.enemies The currently selected enemies in the encounter
 * @param {function} props.clearEncounter The function to clear all enemies from the encounter
 * @param {function} props.handleLoad The function to select an encounter's enemies
 * @returns {JSX.Element}
 */
export default function EncounterControls({
  enemies,
  clearEncounter,
  handleLoad,
}) {
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
    <Space direction="vertical" style={{ width: "100%" }} size="middle">
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12}>
          <SavedEncounters handleLoad={handleLoad} />
        </Col>
        <Col xs={24} sm={12}>
          <Button type="primary" danger onClick={clearEncounter} block>
            Clear Encounter
          </Button>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24}>
          <Space.Compact style={{ width: "100%" }}>
            <Input
              type="text"
              id="name"
              placeholder="Enter encounter name..."
              value={encounterName}
              onChange={handleChange}
              disabled={!user}
              style={{ flex: 1 }}
            />
            <Button
              type="primary"
              onClick={save}
              disabled={!user}
              style={{ width: "auto" }}
            >
              Save
            </Button>
          </Space.Compact>
        </Col>
      </Row>
    </Space>
  );
}
