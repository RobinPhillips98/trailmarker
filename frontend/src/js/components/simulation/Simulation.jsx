// Third-party libraries
import { useContext, useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  Button,
  Collapse,
  FloatButton,
  Grid,
  List,
  Spin,
  Switch,
  Typography,
} from "antd";
import { PlayCircleOutlined } from "@ant-design/icons";

// Personal helpers
import api from "../../api";
import { errorAlert, getRandom, toTitleCase } from "../../services/helpers";

// Contexts
import { AuthContext } from "../../contexts/AuthContext";

/**
 * A page to display the results of a simulation.
 *
 * Loaded by the run simulation button on the homepage, which navigates to
 * "/simulation" while also passing the enemies object with useNavigate.
 *
 *
 * @property {object} enemies The enemies to be included in the encounter
 *
 * @returns {React.ReactElement}
 */
export default function Simulation() {
  // State Variables
  const [simData, setSimData] = useState([{}]);
  const [wins, setWins] = useState();
  const [winsRatio, setWinsRatio] = useState();
  const [totalSims, setTotalSims] = useState();
  const [totalPlayers, setTotalPlayers] = useState();
  const [avgDeaths, setAvgDeaths] = useState();
  const [avgRounds, setAvgRounds] = useState();
  const [loaded, setLoaded] = useState(false);
  const [run, setRun] = useState(false);
  const [switched, setSwitched] = useState(false);

  // Other variables
  const { token } = useContext(AuthContext);
  const navigate = useNavigate();
  const { state } = useLocation();
  const screens = Grid.useBreakpoint();
  const { enemies } = state;
  const { Paragraph, Title } = Typography;

  const simTitle = switched
    ? "Individual Simulation Data"
    : "Sampled Simulation Data";

  // Functions

  /**
   * Toggles the "show all simulations" switch.
   */
  function handleChange() {
    setSwitched(!switched);
  }

  /**
   * Changes the run variable to the opposite of itself, since useEffect
   * depends on run this causes useEffect to run again, running the
   * simulation again.
   */
  function handleClick() {
    setLoaded(false);
    setRun(!run);
  }

  // useEffect calls

  useEffect(() => {
    if (!token) {
      alert("Sorry: You must be logged in to access this page");
      navigate("/login");
    }
  }, [navigate, token]);

  useEffect(() => {
    const request = {
      enemies: enemies.map((enemy) => {
        return {
          id: enemy.id,
          quantity: enemy.quantity,
        };
      }),
    };
    /**
     * Uses the `enemies` object obtained from useLocation to make a POST
     * request to the simulation API endpoint, then sets simData, wins,
     * totalSims, winsRatio, avgDeaths, avgRounds, and totalPlayers using the
     * data returned by the simulation in order to display the results.
     */
    async function callSimulation() {
      try {
        const response = await api.post("/simulation", request, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setSimData(response.data.sim_data);
        setWins(response.data.wins);
        setTotalSims(response.data.total_sims);
        setWinsRatio(response.data.wins_ratio);
        setAvgDeaths(response.data.average_deaths);
        setAvgRounds(response.data.average_rounds);
        setTotalPlayers(response.data.sim_data[0].total_players);
        setLoaded(true);
      } catch (error) {
        errorAlert("Error running simulation", error);
      }
    }
    callSimulation();
  }, [enemies, run, token]);

  if (loaded) {
    const randomSimData = getRandom(simData, 10).sort(
      (a, b) => a.sim_num - b.sim_num,
    );

    const simDataToUse = switched ? simData : randomSimData;

    const simDataDisplay = simDataToUse.map((sim, i) => {
      return {
        key: `sim_${i + 1}`,
        label: `Simulation ${sim.sim_num} - Winner: ${toTitleCase(
          sim.winner,
        )}!`,
        children: (
          <div
            style={{
              maxHeight: screens.md ? 500 : 300,
              overflow: "auto",
            }}
          >
            <Title level={2}>Overview</Title>
            <Paragraph>
              Players killed: {sim.players_killed}/{totalPlayers}
            </Paragraph>
            <Paragraph>Rounds taken: {sim.rounds}</Paragraph>
            <Title level={2}>Combat Log:</Title>

            {sim.log.map((message, index) => {
              if (message.includes("won")) {
                return (
                  <Title key={`log_message_${index}`} level={2}>
                    {message}
                  </Title>
                );
              } else if (
                message.includes("Party") ||
                message.includes("Enemies") ||
                message.includes("Initiative") ||
                message.includes("Round")
              ) {
                return (
                  <Title key={`log_message_${index}`} level={3}>
                    {message}
                  </Title>
                );
              } else if (message.includes("turn")) {
                return (
                  <Title key={`log_message_${index}`} level={4}>
                    {message}
                  </Title>
                );
              } else if (message.includes("Hit") || message.includes("Miss")) {
                return (
                  <Paragraph key={`log_message_${index}`} italic>
                    {message}
                  </Paragraph>
                );
              } else if (
                message.includes("died") ||
                message.includes("critical")
              ) {
                return (
                  <Paragraph key={`log_message_${index}`} strong>
                    {message}
                  </Paragraph>
                );
              } else
                return (
                  <Paragraph key={`log_message_${index}`}>{message}</Paragraph>
                );
            })}
          </div>
        ),
      };
    });

    return (
      <>
        <Title>Simulation Results</Title>
        <Button
          type="primary"
          onClick={handleClick}
          icon={<PlayCircleOutlined />}
        >
          Run Again
        </Button>
        <Title level={2}>
          Players won {wins}/{totalSims} simulations ({winsRatio.toFixed(0)}%)
        </Title>
        <List bordered style={{ maxWidth: screens.md ? 350 : "100%" }}>
          <List.Item>
            Average Number of Players Killed: {avgDeaths}/{totalPlayers}
          </List.Item>
          <List.Item>Average Number of Rounds: {avgRounds}</List.Item>
        </List>
        <Title level={2}>Show data for all simulations?</Title>
        <Switch checked={switched} onChange={handleChange} />
        <Title level={2}>{simTitle}:</Title>
        <Collapse
          accordion
          items={simDataDisplay}
          style={
            switched
              ? {
                  maxHeight: screens.md ? 600 : "none",
                  overflow: screens.md ? "auto" : "visible",
                }
              : null
          }
          size="large"
        />
        <FloatButton.BackTop />
      </>
    );
  } else {
    return <Spin size="large" />;
  }
}
