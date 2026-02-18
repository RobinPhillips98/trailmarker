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

import api from "../../api";
import { AuthContext } from "../../contexts/AuthContext";
import { errorAlert, getRandom, toTitleCase } from "../../services/helpers";

/**
 * A page to display the results of a simulation.
 *
 * Loaded by the run simulation button on the homepage, which navigates to
 * "/simulation" while also passing the enemies object with useNavigate.
 *
 *
 * @property {object} enemies The enemies to be included in the encounter
 *
 * @returns {JSX.Element}
 */
export default function Simulation() {
  const { token } = useContext(AuthContext);
  const navigate = useNavigate();
  const { state } = useLocation();
  const { enemies } = state;
  const { useBreakpoint } = Grid;
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
  const { Paragraph, Title } = Typography;
  const screens = useBreakpoint();

  function handleChange() {
    setSwitched(!switched);
  }

  const simTitle = switched
    ? "Individual Simulation Data"
    : "Sampled Simulation Data";

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
     * Uses the passed in enemies object to make a POST request to the
     * simulation API endpoint, then sets simData, wins, and totalSims to
     * the data returned by the simulation in order to display the results.
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
        setWinsRatio((response.data.wins / response.data.total_sims) * 100);
        setAvgDeaths(
          response.data.sim_data.reduce(
            (acc, current) => acc + current.players_killed,
            0,
          ) / response.data.total_sims,
        );
        setAvgRounds(
          response.data.sim_data.reduce(
            (acc, current) => acc + current.rounds,
            0,
          ) / response.data.total_sims,
        );
        setTotalPlayers(response.data.sim_data[0].total_players);
        setLoaded(true);
      } catch (error) {
        errorAlert("Error running simulation", error);
      }
    }
    callSimulation();
  }, [enemies, run, token]);

  /**
   * Changes the run variable to the opposite of itself, since useEffect
   * depends on run this causes useEffect to run again, running the
   * simulation again.
   */
  function handleClick() {
    setLoaded(false);
    setRun(!run);
  }

  if (loaded) {
    const randomSimData = getRandom(simData, 10).sort(
      (a, b) => a.sim_num - b.sim_num,
    );

    const simDataToUse = switched ? simData : randomSimData;

    const simDataDisplay = simDataToUse.map((sim, i) => {
      return {
        key: i + 1,
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
            {sim.log.map((message) => {
              if (message.includes("won")) {
                return <Title level={2}>{message}</Title>;
              } else if (
                message.includes("Party") ||
                message.includes("Enemies") ||
                message.includes("Initiative") ||
                message.includes("Round")
              ) {
                return <Title level={3}>{message}</Title>;
              } else if (message.includes("turn")) {
                return <Title level={4}>{message}</Title>;
              } else if (message.includes("Hit") || message.includes("Miss")) {
                return <Paragraph italic>{message}</Paragraph>;
              } else if (
                message.includes("died") ||
                message.includes("critical")
              ) {
                return <Paragraph strong>{message}</Paragraph>;
              } else return <Paragraph>{message}</Paragraph>;
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
    return <Spin tip="Loading..." size="large" />;
  }
}
