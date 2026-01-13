import { Button, Card, Form, Input, InputNumber, Select } from "antd";
import { MinusOutlined, PlusOutlined } from "@ant-design/icons";

import { damageTypes } from "../../characterHelpers";

/**
 * A component to allow a user to add attacks to a player character
 *
 * @param {object} props
 * @param {boolean} props.editing True if this is a saved character being edited, false if this is a new character
 * @param {object} props.savedCharacter The character being edited
 * @returns {JSX.element}
 */
export default function AttacksSelection({ editing, savedCharacter }) {
  const initialAttacks = editing
    ? savedCharacter.actions.attacks.map((attack) => ({
        name: attack.name,
        attackBonus: attack.attackBonus,
        damage: attack.damage,
        damageType: attack.damageType,
      }))
    : [{}];

  return (
    <Card title="Attacks" style={{ marginLeft: 100, width: 300 }}>
      {/* Allow user to add as many attacks as they want, with each attack
      having the same style of input */}
      <Form.List name={["actions", "attacks"]} initialValue={initialAttacks}>
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
                <Form.Item
                  {...restField}
                  name={[name, "attackBonus"]}
                  label="Attack Bonus"
                  labelCol={{ span: 24 }}
                  rules={[
                    {
                      required: true,
                      message: "Please input an attack bonus",
                    },
                  ]}
                >
                  <InputNumber min={-5} max={30} style={{ width: 100 }} />
                </Form.Item>
                <Form.Item
                  {...restField}
                  name={[name, "damage"]}
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
                <Form.Item
                  {...restField}
                  name={[name, "damageType"]}
                  label="Damage Type"
                  labelCol={{ span: 24 }}
                  rules={[
                    { required: true, message: "Please input a damage type" },
                  ]}
                >
                  <Select options={damageTypes} style={{ width: 125 }} />
                </Form.Item>
                <Button
                  type="dashed"
                  icon={<MinusOutlined />}
                  onClick={() => remove(name)}
                >
                  Remove Attack
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
                Add attack
              </Button>
            </Form.Item>
          </>
        )}
      </Form.List>
    </Card>
  );
}
