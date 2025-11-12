import SelectedEnemy from "./SelectedEnemy";
import EncounterOptions from "./EncounterOptions";
import { List } from "antd";

function EncounterDisplay(props) {
  return (
    <div>
      <EncounterOptions
        enemies={props.enemies}
        clearEncounter={props.clearEncounter}
      />
      <List
        header={<h2>Encounter</h2>}
        bordered={true}
        size="small"
      >
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
