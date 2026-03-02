import { Button, Card, Col, Form, Input, InputNumber, Row, Select } from "antd";
import { MinusOutlined } from "@ant-design/icons";

import {
  areaTypes,
  damagePattern,
  damageTypes,
  saveOptions,
} from "../../characterHelpers";

/**
 * A sub-component for a single spell entry.
 *
 * Required so that Form.useWatch can be called at this level (hooks must be
 * called at the component level, not inside a render prop).
 *
 * @typedef {object} SpellItemProps
 * @property {string} name The name of the spell
 * @property {object} restField Ant Design Form.List fields
 * @property {function} remove The function to remove a SpellItem
 * @property {FormInstance} form The Ant Design form instance
 *
 * @param {SpellItemProps} props
 * @returns {React.ReactElement}
 */
export default function SpellItem(props) {
  const { name, restField, remove, form } = props;
  const areaType = Form.useWatch(
    ["actions", "spells", name, "area", "type"],
    form,
  );

  return (
    <Card size="small" style={{ marginBottom: 12 }}>
      <Form.Item
        {...restField}
        name={[name, "name"]}
        label="Name"
        rules={[{ required: true, message: "Please input a name" }]}
      >
        <Input />
      </Form.Item>
      <Row gutter={12}>
        <Col span={12}>
          <Form.Item
            {...restField}
            name={[name, "slots"]}
            label="Slots Prepared"
            rules={[
              {
                required: true,
                message: "Please input a number of slots",
              },
            ]}
          >
            <InputNumber style={{ width: "100%" }} min={0} max={3} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item
            {...restField}
            name={[name, "level"]}
            label="Level"
            rules={[
              {
                required: true,
                message: "Please input a level",
              },
            ]}
          >
            <InputNumber style={{ width: "100%" }} min={0} max={2} />
          </Form.Item>
        </Col>
      </Row>
      <Row gutter={12}>
        <Col span={12}>
          <Form.Item
            {...restField}
            name={[name, "damage_roll"]}
            label="Damage"
            rules={[
              { required: true, message: "Please input a damage" },
              {
                pattern: damagePattern,
                message: "Input must be a valid damage roll (ex. 1d4 or 1d8+4)",
              },
            ]}
          >
            <Input placeholder="1d8+4" />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item
            {...restField}
            name={[name, "damage_type"]}
            label="Damage Type"
            rules={[
              {
                required: true,
                message: "Please input a damage type",
              },
            ]}
          >
            <Select
              showSearch={{ optionFilterProp: "label" }}
              options={damageTypes}
              style={{ width: "100%" }}
            />
          </Form.Item>
        </Col>
      </Row>
      <Row gutter={12}>
        <Col span={12}>
          <Form.Item
            {...restField}
            name={[name, "range"]}
            label="Range"
            rules={[{ required: true, message: "Please input a range" }]}
          >
            <InputNumber min={5} max={1000} />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item {...restField} name={[name, "targets"]} label="Targets">
            <InputNumber min={0} max={10} />
          </Form.Item>
        </Col>
      </Row>
      <Row gutter={12}>
        <Col span={12}>
          <Form.Item
            {...restField}
            name={[name, "area", "type"]}
            label="Area type"
          >
            <Select options={areaTypes} allowClear />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item
            {...restField}
            name={[name, "area", "value"]}
            label="Area value"
            rules={[
              {
                required: areaType,
                message: "Please input an area value",
              },
            ]}
          >
            <InputNumber min={0} max={500} />
          </Form.Item>
        </Col>
      </Row>
      <Row gutter={12}>
        <Col span={12}>
          <Form.Item {...restField} name={[name, "save"]} label="Saving Throw">
            <Select
              allowClear
              options={saveOptions}
              style={{ width: "100%" }}
            />
          </Form.Item>
        </Col>
        <Col span={12}>
          <Form.Item
            {...restField}
            name={[name, "actions"]}
            label="Action Cost"
            rules={[
              { required: true, message: "Please input an action cost" },
              {
                pattern: /^[0123]( to [23])?$/i,
                message:
                  "Input must be a valid number of actions (ex. '1' or '1 to 3')",
              },
            ]}
          >
            <Input placeholder="1 to 3" />
          </Form.Item>
        </Col>
      </Row>

      <Button
        type="dashed"
        icon={<MinusOutlined />}
        onClick={() => remove(name)}
      >
        Remove Spell
      </Button>
    </Card>
  );
}
