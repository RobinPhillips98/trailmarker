import { Button, Card, Col, Form, Input, InputNumber, Row, Select } from "antd";
import { MinusOutlined, PlusOutlined } from "@ant-design/icons";
import { damageTypes } from "../../characterHelpers";

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
      }))
    : [{}];
  return (
    <Card title="Spells" style={{ marginLeft: 100, width: 300 }}>
      {/* Allow user to add as many spells as they want, with each spell
      having the same style of input */}
      <Form.List name={["actions", "spells"]} initialValue={initialSpells}>
        {(fields, { add, remove }) => (
          <>
            {fields.map(({ name, ...restField }) => (
              <Card>
                <Form.Item
                  {...restField}
                  name={[name, "name"]}
                  label="Name"
                  labelCol={{ span: 24 }}
                  rules={[{ required: true, message: "Please input a name" }]}
                >
                  <Input style={{ width: 200 }} />
                </Form.Item>
                <Row>
                  <Col span={12}>
                    <Form.Item
                      {...restField}
                      name={[name, "slots"]}
                      label="Slots Prepared"
                      labelCol={{ span: 24 }}
                      rules={[
                        {
                          required: true,
                          message: "Please input a number of slots",
                        },
                      ]}
                    >
                      <InputNumber style={{ width: 100 }} min={0} max={3} />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      {...restField}
                      name={[name, "level"]}
                      label="Level"
                      labelCol={{ span: 24 }}
                      rules={[
                        {
                          required: true,
                          message: "Please input a level",
                        },
                      ]}
                    >
                      <InputNumber style={{ width: 50 }} min={0} max={2} />
                    </Form.Item>
                  </Col>
                </Row>
                <Row>
                  <Col span={12}>
                    <Form.Item
                      {...restField}
                      name={[name, "damage_roll"]}
                      label="Damage"
                      labelCol={{ span: 24 }}
                      rules={[
                        { required: true, message: "Please input a damage" },
                        {
                          pattern: /^\dd(4|6|8|10|12)([+-]\d{1,2})?$/i,
                          message:
                            "Input must be a valid damage roll (ex. 1d4 or 1d8+4)",
                        },
                      ]}
                    >
                      <Input style={{ width: 100 }} placeholder="1d8+4" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      {...restField}
                      name={[name, "damage_type"]}
                      label="Damage Type"
                      labelCol={{ span: 24 }}
                      rules={[
                        {
                          required: true,
                          message: "Please input a damage type",
                        },
                      ]}
                    >
                      <Select options={damageTypes} style={{ width: 125 }} />
                    </Form.Item>
                  </Col>
                </Row>
                <Row>
                  <Col span={12}>
                    <Form.Item
                      {...restField}
                      name={[name, "range"]}
                      label="Range"
                      labelCol={{ span: 24 }}
                      rules={[
                        { required: true, message: "Please input a range" },
                      ]}
                    >
                      <Input style={{ width: 100 }} placeholder="120 feet" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      {...restField}
                      name={[name, "target"]}
                      label="Target"
                      labelCol={{ span: 24 }}
                      rules={[
                        { required: true, message: "Please input a target" },
                      ]}
                    >
                      <Input style={{ width: 100 }} placeholder="1 creature" />
                    </Form.Item>
                  </Col>
                </Row>
                <Row>
                  <Col span={12}>
                    <Form.Item
                      {...restField}
                      name={[name, "area", "type"]}
                      label="Area type"
                      labelCol={{ span: 24 }}
                    >
                      <Input style={{ width: 100 }} placeholder="emanation" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      {...restField}
                      name={[name, "area", "value"]}
                      label="Area value"
                      labelCol={{ span: 24 }}
                    >
                      <Input style={{ width: 100 }} placeholder="15 feet" />
                    </Form.Item>
                  </Col>
                </Row>
                <Form.Item
                  {...restField}
                  name={[name, "actions"]}
                  label="Action Cost"
                  labelCol={{ span: 24 }}
                  rules={[
                    { required: true, message: "Please input a damage" },
                    {
                      pattern: /^[012]( to [23])?$/i,
                      message:
                        "Input must be a valid number of actions (ex. '1' or '1 to 3')",
                    },
                  ]}
                >
                  <Input style={{ width: 100 }} placeholder="1 to 3" />
                </Form.Item>

                <Button
                  type="dashed"
                  icon={<MinusOutlined />}
                  onClick={() => remove(name)}
                >
                  Remove Spell
                </Button>
              </Card>
            ))}
            <br />
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
