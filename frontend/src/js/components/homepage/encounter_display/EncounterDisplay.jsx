import { List, Typography } from "antd";

import SelectedEnemy from "./SelectedEnemy";

/**
 *
 * A component to display the currently built encounter
 *
 * @typedef {object} EncounterDisplayProps
 * @property {array} enemies The list of selected enemies to render the encounter display from
 * @property {function} handleRemove The function called when remove is clicked
 * @property {function} handleDecrement The function called when the minus button is clicked
 * @property {function} handleAdd The function called when the plus button is clicked
 *
 * @param {EncounterDisplayProps} props
 * @returns {JSX.Element}
 */
export default function EncounterDisplay(props) {
  const { enemies, handleRemove, handleDecrement, handleAdd } = props;
  const { Title } = Typography;

  return (
    <div>
      <List
        header={<Title level={3}>Encounter</Title>}
        bordered={true}
        size="small"
        style={{ maxHeight: 300, overflow: "scroll" }}
      >
        {enemies.map((enemy) => (
          <List.Item key={enemy.id}>
            <SelectedEnemy
              enemy={enemy}
              handleRemove={handleRemove}
              handleDecrement={handleDecrement}
              handleAdd={handleAdd}
            />
          </List.Item>
        ))}
      </List>
    </div>
  );
}
