import { Button, Card, Form } from "antd";
import { PlusOutlined } from "@ant-design/icons";

import SpellItem from "./SpellsSelection.Item";

/**
 * A component to allow a user to add spells to a player character
 *
 * @param {object} props
 * @param {boolean} props.editing True if this is a saved character being
 *  edited, false if this is a new character.
 * @param {object} props.savedCharacter The character being edited, if any.
 * @returns {React.ReactElement}
 */
export default function SpellsSelection({ editing, savedCharacter }) {
  const form = Form.useFormInstance();

  const initialSpells = editing
    ? savedCharacter.actions.spells.map((spell) => ({
        name: spell.name,
        slots: spell.slots,
        level: spell.level,
        damage_roll: spell.damage_roll,
        damage_type: spell.damage_type,
        range: spell.range,
        area: spell.area,
        targets: spell.targets,
        actions: spell.actions,
        save: spell.save,
      }))
    : [];

  return (
    <Card title="Offensive Spells" style={{ width: "100%" }}>
      {/* Allow user to add as many spells as they want, with each spell
      having the same style of input */}
      <Form.List name={["actions", "spells"]} initialValue={initialSpells}>
        {(fields, { add, remove }) => (
          <>
            {fields.map(({ key, name, ...restField }) => (
              <SpellItem
                key={key}
                name={name}
                restField={restField}
                remove={remove}
                form={form}
              />
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
