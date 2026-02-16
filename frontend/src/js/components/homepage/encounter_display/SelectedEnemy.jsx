import { Button, Space, Row, Col, Typography } from "antd";
import { MinusOutlined, PlusOutlined, DeleteOutlined } from "@ant-design/icons";

/**
 *
 * A component to display an enemy that has been selected in the current encounter
 *
 * @typedef {object} SelectedEnemyProps
 * @property {object} enemy The enemy to be displayed
 * @property {function} handleRemove The function called when remove is clicked
 * @property {function} handleDecrement The function called when the minus button is clicked
 * @property {function} handleAdd The function called when the plus button is clicked
 *
 * @param {SelectedEnemyProps} props
 * @returns {JSX.Element}
 */
export default function SelectedEnemy(props) {
  const { enemy, handleRemove, handleDecrement, handleAdd } = props;
  const { Text } = Typography;

  function handleClickDecrement() {
    handleDecrement(enemy);
  }

  function handleClickRemove() {
    handleRemove(enemy);
  }

  function handleClickAdd() {
    handleAdd(enemy);
  }

  return (
    <Row
      style={{ width: "100%" }}
      gutter={[12, 16]}
      align="middle"
      justify="space-between"
    >
      <Col xs={24} sm={12}>
        <Text style={{ fontSize: "16px", fontWeight: "bold" }}>
          {enemy.name}
        </Text>
      </Col>
      <Col xs={24} sm={12}>
        <Space
          size="middle"
          wrap
          style={{ width: "100%", justifyContent: "flex-end" }}
        >
          <Button
            size="large"
            icon={<MinusOutlined />}
            style={{ backgroundColor: "#c74a4a", color: "#fff" }}
            variant="solid"
            onClick={handleClickDecrement}
          />
          <Text
            style={{ fontSize: "18px", minWidth: "40px", textAlign: "center" }}
          >
            {enemy.quantity}
          </Text>
          <Button
            size="large"
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleClickAdd}
          />
          <Button
            size="large"
            type="primary"
            danger
            icon={<DeleteOutlined />}
            onClick={handleClickRemove}
          />
        </Space>
      </Col>
    </Row>
  );
}
