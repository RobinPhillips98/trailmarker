import Enemy from "./Enemy";
import api from "../../api";
import { useEffect, useState } from "react";

function EnemyList(props) {
  const [enemies, setEnemies] = useState([]);

  const fetchEnemies = async () => {
    try {
      const response = await api.get('/enemies');
      setEnemies(response.data.enemies);
    } catch (error) {
      console.error("Error fetching enemies", error);
    }
  };

  useEffect(() => {
    fetchEnemies()
  }, [])

  return (
    <div id="enemyList">
      <h2>Enemies</h2>
      <ul>
        {enemies.map((enemy) => (
          <li key={enemy.id}>
            <Enemy handleAdd={props.handleAdd} enemy={enemy} />
          </li>
        ))}
      </ul>
    </div>
  );
}

export default EnemyList;
