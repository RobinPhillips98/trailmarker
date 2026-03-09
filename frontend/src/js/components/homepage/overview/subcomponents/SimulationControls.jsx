// Third-party libraries
import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Card, Col, Row, Switch, Tooltip, Typography } from "antd";
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
 * @typedef {object} SimulationControlsProps
 * @property {object} selectedEnemies The currently selected enemies in the
 *  encounter
 * @property {boolean} charactersSaved Whether or not the current user has
 *  any saved characters
 * @property {React.RefObject[]} refs References used by the opening tour to
 * target components
 *
 * @param {SimulationControlsProps} props
 * @returns {React.ReactElement}
 */
export default function SimulationControls(props) {
  const { selectedEnemies, charactersSaved, refs } = props;
  const { user } = useContext(AuthContext);

  const switchDisabled = !user || !charactersSaved;
  const [switched, setSwitched] = useState(switchDisabled);

  const navigate = useNavigate();
  const { Text } = Typography;

  const simButtonDisabled = isEmpty(selectedEnemies);

  let switchTooltip = "";
  if (!user) switchTooltip = "Must be signed in to use custom characters";
  else if (!charactersSaved) {
    switchTooltip = "No characters saved!";
  } else {
    switchTooltip = "";
  }

  // Switch needs to be set back to true when user logs out
  useEffect(() => {
    if (switchDisabled) setSwitched(true);
    else setSwitched(false);
  }, [switchDisabled]);

  /**
   * Runs the simulation by navigating to the simulation page.
   */
  function handleClick() {
    navigate("/simulation/", {
      state: { enemies: selectedEnemies, pregen_chars: switched },
    });
  }

  return (
    <Row
      gutter={[16, 16]}
      style={{ marginBottom: 24 }}
      justify="center"
      align="middle"
    >
      {/* Empty column to keep Run Simulation button centered*/}
      <Col xs={0} md={8} />

      <Col xs={24} md={8}>
        <Tooltip
          title={
            simButtonDisabled
              ? "Must select enemies before running simulation"
              : null
          }
        >
          <Button
            type="primary"
            size="large"
            block
            onClick={handleClick}
            disabled={simButtonDisabled}
            icon={
              !simButtonDisabled ? <PlayCircleOutlined /> : <LockOutlined />
            }
            ref={refs[7]}
          >
            Run Simulation
          </Button>
        </Tooltip>
      </Col>

      <Col xs={24} md={8}>
        <Card ref={refs[6]} title="Simulation Options">
          <Tooltip title={switchTooltip}>
            <Switch
              checked={switched}
              disabled={switchDisabled}
              onChange={() => setSwitched(!switched)}
              checkedChildren={<CheckOutlined />}
              unCheckedChildren={<CloseOutlined />}
            />
          </Tooltip>
          <Text style={{ marginLeft: 5 }}>Use generic characters</Text>
        </Card>
      </Col>
    </Row>
  );
}
