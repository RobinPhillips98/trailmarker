import { Button, Card, Col, Form, Input, InputNumber, Row, Select } from "antd";
import { MinusOutlined, PlusOutlined } from "@ant-design/icons";
import { areaTypes, damageTypes, saveOptions } from "../../characterHelpers";

/**
 * A component to allow a user to add spells to a player character
 *
 * @param {object} props
 * @param {boolean} props.editing True if this is a saved character being
 *  edited, false if this is a new character
 * @param {object} props.savedCharacter The character being edited
 * @returns {JSX.element}
 */
export default function SpellsSelection({ editing, savedCharacter }) {
  const initialSpells = editing
    ? savedCharacter.actions.spells.map((spell) => ({
        name: spell.name,
        slots: spell.slots,
        level: spell.level,
        damage_roll: spell.damage_roll,
        damage_type: spell.damage_type,
        range: spell.range,
        area: spell.area,
        target: spell.target,
        actions: spell.actions,
        save: spell.save,
      }))
    : [{}];

  return (
    <Card title="Spells" style={{ width: "100%" }}>
      {/* Allow user to add as many spells as they want, with each spell
      having the same style of input */}
      <Form.List name={["actions", "spells"]} initialValue={initialSpells}>
        {(fields, { add, remove }) => (
          <>
            {fields.map(({ name, ...restField }) => (
              <Card key={name} size="small" style={{ marginBottom: 12 }}>
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
                          pattern: /^\dd(4|6|8|10|12)([+-]\d{1,2})?$/i,
                          message:
                            "Input must be a valid damage roll (ex. 1d4 or 1d8+4)",
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
                      rules={[
                        { required: true, message: "Please input a range" },
                      ]}
                    >
                      <Input placeholder="120 feet" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      {...restField}
                      name={[name, "target"]}
                      label="Target"
                    >
                      <Input placeholder="1 creature" />
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
                      {/* <Input placeholder="emanation" /> */}
                      <Select options={areaTypes} allowClear />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      {...restField}
                      name={[name, "area", "value"]}
                      label="Area value"
                    >
                      <Input placeholder="15 feet" />
                    </Form.Item>
                  </Col>
                </Row>
                <Row gutter={12}>
                  <Col span={12}>
                    <Form.Item
                      {...restField}
                      name={[name, "save"]}
                      label="Saving Throw"
                    >
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
                        { required: true, message: "Please input a damage" },
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
            ))}
            <Form.Item>
              <Button
                type="dashed"
                onClick={() => add()}
                block
                icon={<PlusOutlined />}
              >
                Add Spell
              </Button>
            </Form.Item>
          </>
        )}
      </Form.List>
    </Card>
  );
}
