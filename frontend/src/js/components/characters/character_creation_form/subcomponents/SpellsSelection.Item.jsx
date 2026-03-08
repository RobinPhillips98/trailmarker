import { Button, Col, Form, InputNumber, Row, Select } from "antd";
import { MinusOutlined } from "@ant-design/icons";

import { spellOptions } from "../../characterHelpers";

/**
 * A sub-component for a single spell entry.
 *
 * @typedef {object} SpellItemProps
 * @property {number} name The Form.List field name (index)
 * @property {object} restField Ant Design Form.List fields
 * @property {function} remove The function to remove this SpellItem
 *
 * @param {SpellItemProps} props
 * @returns {React.ReactElement}
 */
export default function SpellItem({ name, restField, remove }) {
  return (
    <Row gutter={12} style={{ marginBottom: 12 }} align="middle">
      <Col span={14}>
        <Form.Item
          {...restField}
          name={[name, "key"]}
          rules={[{ required: true, message: "Please select a spell" }]}
          style={{ marginBottom: 0 }}
        >
          <Select
            showSearch={{ optionFilterProp: "label" }}
            options={spellOptions}
            placeholder="Select a spell"
            style={{ width: "100%" }}
          />
        </Form.Item>
      </Col>
      <Col span={6}>
        <Form.Item
          {...restField}
          name={[name, "slots"]}
          rules={[{ required: true, message: "Please input slots" }]}
          style={{ marginBottom: 0 }}
        >
          <InputNumber
            min={1}
            max={3}
            placeholder="Slots"
            style={{ width: "100%" }}
          />
        </Form.Item>
      </Col>
      <Col span={4}>
        <Button
          type="dashed"
          icon={<MinusOutlined />}
          onClick={() => remove(name)}
          style={{ width: "100%" }}
        />
      </Col>
    </Row>
  );
}
