import { Card, Empty, List, Typography } from "antd";

import SelectedEnemy from "./SelectedEnemy";

/**
 *
 * A component to display the currently built encounter
 *
 * @typedef {object} EncounterDisplayProps
 * @property {array} enemies The list of selected enemies to render the
 *  encounter display from
 * @property {function} handleRemove The function called when remove is clicked
 * @property {function} handleDecrement The function called when the minus
 *  button is clicked
 * @property {function} handleAdd The function called when the plus button is
 *  clicked
 *
 * @param {EncounterDisplayProps} props
 * @returns {React.ReactElement}
 */
export default function EncounterDisplay(props) {
  const { enemies, handleRemove, handleDecrement, handleAdd } = props;
  const { Title } = Typography;

  return (
    <Card>
      <Title level={4} style={{ marginTop: 0, marginBottom: 16 }}>
        Encounter
      </Title>
      <List
        bordered
        size="large"
        style={{
          maxHeight: "35vh",
          overflow: "auto",
        }}
        dataSource={enemies}
        locale={{ emptyText: <Empty description="No enemies selected" /> }}
        renderItem={(enemy) => (
          <List.Item style={{ padding: "16px" }}>
            <SelectedEnemy
              enemy={enemy}
              handleRemove={handleRemove}
              handleDecrement={handleDecrement}
              handleAdd={handleAdd}
            />
          </List.Item>
        )}
      />
    </Card>
  );
}
