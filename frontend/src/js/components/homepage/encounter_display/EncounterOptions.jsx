import api from "../../../api";
import { useContext, useState } from "react";
import { Button, Input, Space, Typography } from "antd";
import { AuthContext } from "../../../contexts/AuthContext";
const { Title } = Typography;

function EncounterOptions(props) {
  const [encounterName, setEncounterName] = useState("");

  const handleChange = (event) => {
    setEncounterName(event.target.value);
  };

  const { user, token } = useContext(AuthContext);

  async function save() {
    if (props.enemies.length === 0) {
      alert("Encounter is empty, please add enemies.");
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

    await api.post("/encounters", encounter, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    setEncounterName("");
  }

  if (user) {
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
          />
        </Space.Compact>
        <br />
        <Button danger onClick={props.clearEncounter}>
          Clear Encounter
        </Button>
      </div>
    );
  } else {
    return (
      <>
        <Title level={4}>Please login to save encounters</Title>
        <br />
        <Button danger onClick={props.clearEncounter}>
          Clear Encounter
        </Button>
      </>
    );
  }
}

export default EncounterOptions;
