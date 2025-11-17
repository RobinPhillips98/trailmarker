import { Card, Form, InputNumber } from "antd";
import { saves, toTitleCase } from "../characterHelpers";

export default function SavesSelection() {
  return (
    <Card
        title="Saving Throws"
        size="small"
        style={{ marginLeft: 100, width: 300 }}
        variant="borderless"
      >
        {saves.map((save) => (
          <Form.Item
            label={toTitleCase(save)}
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
  )
}