import Enemy from "./Enemy";
import api from "../../../api";
import { useEffect, useState } from "react";
import { List } from "antd";

function EnemyList(props) {
  const [enemies, setEnemies] = useState([]);

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
      header={<h2>Enemies</h2>}
      bordered={true}
      style={{ marginTop: 10, height: 900, overflow: "scroll" }}
      grid={{ gutter: 16, column: 5 }}
      dataSource={enemies}
      renderItem={(enemy) => (
        <List.Item>
          <Enemy handleAdd={props.handleAdd} enemy={enemy} />
        </List.Item>
      )}
    />
  );
}

export default EnemyList;
