import { Card, Col, Form, InputNumber, Row } from "antd";

import { attributes } from "../../characterHelpers";
import { toTitleCase } from "../../../../services/helpers";

/**
 * A component to allow a user to set a player character's attribute modifiers
 *
 * @param {object} props
 * @param {boolean} props.editing True if this is a saved character being
 *  edited, false if this is a new character.
 * @param {object} props.savedCharacter The character being edited, if any.
 * @returns {React.ReactElement}
 */
export default function AttributeSelection({ editing, savedCharacter }) {
  return (
    <Card title="Attribute Modifiers" style={{ width: "100%" }}>
      <Row>
        {attributes.slice(0, 3).map((attribute) => (
          <Col key={`${attribute}_col`} span={8}>
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
          </Col>
        ))}
      </Row>
      <Row>
        {attributes.slice(3, 6).map((attribute) => (
          <Col key={`${attribute}_col`} span={8}>
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
          </Col>
        ))}
      </Row>
    </Card>
  );
}
