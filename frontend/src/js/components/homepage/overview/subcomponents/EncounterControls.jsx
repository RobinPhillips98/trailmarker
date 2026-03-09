// Third-party libraries
import { useContext, useState } from "react";
import { App, Button, Col, Grid, Input, Row, Space, Tooltip } from "antd";
import { ClearOutlined, LockOutlined, SaveOutlined } from "@ant-design/icons";

// Personal helpers
import api from "../../../../api";
import useErrorMessage from "../../../../services/hooks/useErrorMessage";

// Contexts
import { AuthContext } from "../../../../contexts/AuthContext";

// Components
import SavedEncounters from "./saved_encounters/SavedEncounters";

/**
 * A component to display controls for saving, loading, and clearing encounters
 *
 * @typedef {object} EncounterControlsProps
 * @property {object} enemies The currently selected enemies in the encounter
 * @property {function} clearEncounter The function to clear all enemies
 *  from the encounter
 * @property {function} handleLoad The function to select an encounter's
 *  enemies
 *
 * @param {EncounterControlsProps} props
 * @returns {React.ReactElement}
 */
export default function EncounterControls(props) {
  const { enemies, clearEncounter, handleLoad } = props;
  const [encounterName, setEncounterName] = useState("");

  const { user, token } = useContext(AuthContext);
  const { errorMessage } = useErrorMessage();
  const { message } = App.useApp();
  const screens = Grid.useBreakpoint();

  const encounterEmpty = enemies.length === 0;
  const cannotSave = !user || encounterEmpty;

  function handleChange(event) {
    setEncounterName(event.target.value);
  }

  /**
   * Saves the given encounter to the database
   *
   * @returns {void}
   */
  async function save() {
    if (encounterEmpty) {
      message.warning("Encounter is empty, please add enemies.");
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
      message.success("Encounter saved!");
    } catch (error) {
      errorMessage("Failed to save encounter", error);
    }
  }

  return (
    <Space direction="vertical" style={{ width: "100%" }} size="middle">
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12}>
          <SavedEncounters handleLoad={handleLoad} />
        </Col>
        <Col xs={24} sm={12}>
          <Button
            type="primary"
            danger
            onClick={clearEncounter}
            block
            icon={<ClearOutlined />}
          >
            Clear Encounter
          </Button>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24}>
          <Tooltip
            title={!user ? "Must be signed in to save encounters" : ""}
            placement="right"
          >
            <Space.Compact
              style={screens.md ? { width: "50%" } : { width: "100%" }}
            >
              <Input
                type="text"
                id="name"
                placeholder="Enter encounter name..."
                value={encounterName}
                onChange={handleChange}
                disabled={!user}
                style={{ flex: 1 }}
              />
              <Tooltip
                title={
                  user && encounterEmpty // Use above tooltip if not logged in
                    ? "Must select enemies before saving encounter"
                    : ""
                }
                placement="right"
              >
                <Button
                  type="primary"
                  onClick={save}
                  disabled={cannotSave}
                  style={{ width: "auto" }}
                  icon={user ? <SaveOutlined /> : <LockOutlined />}
                >
                  Save Encounter
                </Button>
              </Tooltip>
            </Space.Compact>
          </Tooltip>
        </Col>
      </Row>
    </Space>
  );
}
