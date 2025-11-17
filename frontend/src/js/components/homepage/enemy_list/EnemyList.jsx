import { useEffect, useState } from "react";
import { List, Typography } from "antd";

import api from "../../../api";
import Enemy from "./Enemy";

/**
 * A component to display a list of all enemies from the database
 *
 * @param {object} props
 * @param {function} props.handleAdd The function to add an enemy to the encounter
 * @returns {JSX.Element}
 */
export default function EnemyList({ handleAdd }) {
  const [enemies, setEnemies] = useState([]);
  const { Title } = Typography;

  /**
   * Fetches all enemies from the database
   */
  async function fetchEnemies() {
    try {
      const response = await api.get("/enemies");
      setEnemies(response.data.enemies);
    } catch (error) {
      console.error("Error fetching enemies", error);
    }
  }

  useEffect(() => {
    fetchEnemies();
  }, []);

  return (
    <List
      header={<Title level={3}>Enemies</Title>}
      bordered={true}
      style={{ marginTop: 10, height: "60vh", overflow: "scroll" }}
      grid={{ gutter: 16, column: 5 }}
      dataSource={enemies}
      renderItem={(enemy) => (
        <List.Item>
          <Enemy handleAdd={handleAdd} enemy={enemy} />
        </List.Item>
      )}
    />
  );
}
