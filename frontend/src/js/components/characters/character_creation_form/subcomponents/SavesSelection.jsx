import { Card, Form, InputNumber } from "antd";

import { saves } from "../../characterHelpers";
import { toTitleCase } from "../../../../services/helpers";

/**
 * A component to allow a user to set a player character's saving throws
 *
 * @returns {JSX.element}
 */
export default function SavesSelection() {
  return (
    <Card
      title="Saving Throws"
      style={{ marginLeft: 100, width: 300, height: 300 }}
    >
      {saves.map((save) => (
        <Form.Item
          label={toTitleCase(save)}
          labelCol={{ span: 24 }}
          wrapperCol={{ span: 24 }}
          name={["defenses", "saves", save]}
          rules={[
            {
              required: true,
              message: `Please input a ${save} value`,
            },
          ]}
        >
          <InputNumber min={-5} max={30} />
        </Form.Item>
      ))}
    </Card>
  );
}
