import { useContext, useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../../api";
import { AuthContext } from "../../contexts/AuthContext";
import { isEmpty, toTitleCase } from "../../services/helpers";
import { Collapse, Typography } from "antd";

export default function Simulation() {
  const { token, user } = useContext(AuthContext);
  const navigate = useNavigate();
  const { state } = useLocation();
  const { enemies } = state;
  const [simData, setSimData] = useState({});
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
      console.log(response.data);
      setSimData(response.data);
    }
    callSimulation();
  }, [enemies, token]);

  if (!isEmpty(simData)) {
    const collapseItems = [
      {
        key: "1",
        label: `Winner: ${toTitleCase(simData.winner)}!`,
        // label: (<Title>Winner: {toTitleCase(simData.winner)}!</Title>),
        children: simData.log.map((message) => {
          if (
            message.includes("Party") ||
            message.includes("Enemies") ||
            message.includes("Initiative") ||
            message.includes("Round")
          ) {
            return (
              <Title level={2} style={{ marginTop: 5 }}>
                {message}
              </Title>
            );
          } else return <Paragraph>{message}</Paragraph>;
        }),
      },
    ];

    return <Collapse items={collapseItems} />;
  } else {
    return <Title>Loading, please wait...</Title>;
  }
}
