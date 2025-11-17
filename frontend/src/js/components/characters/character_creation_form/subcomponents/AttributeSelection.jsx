import { Card, Form, InputNumber } from "antd";
import { attributes, toTitleCase } from "../characterHelpers";

export default function AttributeSelection({editing, savedCharacter}) {

  return (
    <Card
        title="Attribute Modifiers"
        size="small"
        style={{ marginLeft: 100, width: 300 }}
        variant="borderless"
      >
        {attributes.map((attribute) => (
          <Form.Item
            key={attribute}
            label={toTitleCase(attribute)}
            name={["attribute_modifiers", attribute]}
            initialValue={
              editing ? savedCharacter.attribute_modifiers[attribute] : 0
            }
            rules={[
              {
                required: true,
                message: `Please input a ${attribute} value`,
              },
            ]}
          >
            <InputNumber min={-2} max={5} />
          </Form.Item>
        ))}
      </Card>
  )
}