import { useContext, useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../../api";
import { AuthContext } from "../../contexts/AuthContext";
import { toTitleCase } from "../../services/helpers";
import { Collapse, Typography } from "antd";

export default function Simulation() {
  const { token, user } = useContext(AuthContext);
  const navigate = useNavigate();
  const { state } = useLocation();
  const { enemies } = state;
  const [simData, setSimData] = useState([{}]);
  const [loaded, setLoaded] = useState(false);
  const { Paragraph, Title } = Typography;

  useEffect(() => {
    if (!token || !user) {
      alert("Sorry: You must be logged in to access this page");
      navigate("/login");
    }
  }, [navigate, token, user]);

  useEffect(() => {
    const request = {
      enemies: enemies.map((enemy) => {
        return {
          id: enemy.id,
          quantity: enemy.quantity,
        };
      }),
    };
    async function callSimulation() {
      const response = await api.post("/simulation", request, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setSimData([response.data]);
      setLoaded(true);
    }
    callSimulation();
  }, [enemies, token]);

  if (loaded) {
    const collapseItems = simData.map((sim, i) => {
      return {
        key: i + 1,
        label: `Simulation ${i + 1} - Winner: ${toTitleCase(sim.winner)}!`,
        children: (
          <>
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
              } else return <Paragraph>{message}</Paragraph>;
            })}
          </>
        ),
      };
    });

    return <Collapse items={collapseItems} />;
  } else {
    return <Title>Loading, please wait...</Title>;
  }
}
