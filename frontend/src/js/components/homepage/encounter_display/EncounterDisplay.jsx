import SelectedEnemy from "./SelectedEnemy";
import { List } from "antd";

function EncounterDisplay(props) {
  return (
    <div>
      <List header={<h2>Encounter</h2>} bordered={true} size="small" style={{maxHeight: 300, overflow: "scroll"}}>
        {props.enemies.map((enemy) => (
          <List.Item key={enemy.id}>
            <SelectedEnemy
              enemy={enemy}
              handleRemove={props.handleRemove}
              handleDecrement={props.handleDecrement}
              handleAdd={props.handleAdd}
            />
          </List.Item>
        ))}
      </List>
    </div>
  );
}

export default EncounterDisplay;
