import { useContext, useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../../api";
import { AuthContext } from "../../contexts/AuthContext";
import { toTitleCase } from "../../services/helpers";
import { Button, Collapse, Typography } from "antd";

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
  const [simData, setSimData] = useState([{}]);
  const [wins, setWins] = useState();
  const [winsRatio, setWinsRatio] = useState();
  const [totalSims, setTotalSims] = useState();
  const [loaded, setLoaded] = useState(false);
  const [run, setRun] = useState(false);
  const { Paragraph, Title } = Typography;

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
      setLoaded(true);
    } catch (error) {
      console.error("Error running simulation", error);
      alert(error.response.statusText);
    }}
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
    const collapseItems = simData.map((sim, i) => {
      return {
        key: i + 1,
        label: `Simulation ${i + 1} - Winner: ${toTitleCase(sim.winner)}!`,
        children: (
          <div style={{ height: 500, overflow: "scroll" }}>
            <Title level={2}>Overview</Title>
            <Paragraph>
              Players killed: {sim.players_killed}/{sim.total_players}
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
              } else if (message.includes("died")) {
                return <Paragraph strong>{message}</Paragraph>;
              } else return <Paragraph>{message}</Paragraph>;
            })}
          </div>
        ),
      };
    });

    return (
      <div>
        <Title>Simulation Results</Title>
        <Button type="primary" onClick={handleClick}>
          Run Again
        </Button>
        <Title level={2}>
          Players won {wins}/{totalSims} simulations ({winsRatio.toFixed(0)}%)
        </Title>
        <Title level={2}>Individual Simulation Data:</Title>
        <Collapse
          accordion
          items={collapseItems}
          style={{ height: 800, overflow: "scroll" }}
          size="large"
        />
      </div>
    );
  } else {
    return <Title>Loading, please wait...</Title>;
  }
}
