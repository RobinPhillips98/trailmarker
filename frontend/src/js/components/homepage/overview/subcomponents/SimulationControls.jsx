// Third-party libraries
import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Col, Row, Switch, Typography } from "antd";
import {
  CheckOutlined,
  CloseOutlined,
  LockOutlined,
  PlayCircleOutlined,
} from "@ant-design/icons";

// Personal Helpers
import { isEmpty } from "../../../../services/helpers";

// Contexts
import { AuthContext } from "../../../../contexts/AuthContext";

/**
 * A component to handle setting options for and starting the simulation.
 *
 * @param {object} props
 * @param {object} props.selectedEnemies The currently selected enemies in the
 *  encounter
 * @param {boolean} props.charactersSaved Whether or not the current user has
 *  any saved characters
 * @returns {React.ReactElement}
 */
export default function SimulationControls({
  selectedEnemies,
  charactersSaved,
}) {
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);
  const { Text } = Typography;
  const simButtonDisabled = isEmpty(selectedEnemies);
  const switchDisabled = !user || !charactersSaved;

  const [switched, setSwitched] = useState(!user);

  useEffect(() => {
    if (!user) setSwitched(true);
  }, [user]);

  /**
   * Runs the simulation by navigating to the simulation page.
   */
  function handleClick() {
    navigate("/simulation/", {
      state: { enemies: selectedEnemies, pregen_chars: switched },
    });
  }

  return (
    <Row gutter={[16, 16]} style={{ marginBottom: 24 }} justify="center">
      {/* Empty column to keep Run Simulation button centered*/}
      <Col xs={0} md={8} />

      <Col xs={24} md={8}>
        <Button
          type="primary"
          size="large"
          block
          onClick={handleClick}
          disabled={simButtonDisabled}
          icon={!simButtonDisabled ? <PlayCircleOutlined /> : <LockOutlined />}
        >
          Run Simulation
        </Button>
      </Col>

      <Col xs={24} md={8}>
        <Switch
          checked={switched}
          disabled={switchDisabled}
          onChange={() => setSwitched(!switched)}
          checkedChildren={<CheckOutlined />}
          unCheckedChildren={<CloseOutlined />}
        />
        <Text style={{ marginLeft: 5 }}>Use pre-generated characters?</Text>
      </Col>
    </Row>
  );
}
