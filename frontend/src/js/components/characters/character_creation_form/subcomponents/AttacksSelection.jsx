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
    <Card
      title="Attacks"
      size="small"
      style={{ marginLeft: 100, width: 300 }}
      variant="borderless"
    >
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
                  rules={[{ required: true, message: "Please input a name" }]}
                >
                  <Input />
                </Form.Item>
                <Form.Item
                  {...restField}
                  name={[name, "attackBonus"]}
                  label="Attack Bonus"
                  rules={[
                    {
                      required: true,
                      message: "Please input an attack bonus",
                    },
                  ]}
                >
                  <InputNumber min={-5} max={30} />
                </Form.Item>
                <Form.Item
                  {...restField}
                  name={[name, "damage"]}
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
                <Form.Item
                  {...restField}
                  name={[name, "damageType"]}
                  label="Damage Type"
                  rules={[
                    { required: true, message: "Please input a damage type" },
                  ]}
                >
                  <Select options={damageTypes} />
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
