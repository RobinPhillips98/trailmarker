import { enemies } from "../../../../assets/dummyData";
import Enemy from "./Enemy";

function EnemyList(props) {
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
