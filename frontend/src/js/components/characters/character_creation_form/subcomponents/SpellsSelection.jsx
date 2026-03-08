import { Button, Card, Form } from "antd";
import { PlusOutlined } from "@ant-design/icons";

import SpellItem from "./SpellsSelection.Item";

/**
 * A component to allow a user to add spells to a player character
 *
 * This approach of converting back and forth from spells_list is necessary
 * in order to use Form.List, since Form.List creates an array which must be
 * transformed back and forth.
 *
 * @param {object} props
 * @param {boolean} props.editing True if this is a saved character being
 *  edited, false if this is a new character.
 * @param {object} props.savedCharacter The character being edited, if any.
 * @returns {React.ReactElement}
 */
export default function SpellsSelection({ editing, savedCharacter }) {
  const initialSpells =
    editing && savedCharacter.actions?.spells
      ? savedCharacter.actions?.spells.map((spell) => ({
          key: spell.name.toLowerCase().replace(/ /g, "_"),
          slots: spell.slots,
        }))
      : [];

  return (
    <Card title="Offensive Spells" style={{ width: "100%" }}>
      <Form.List name={["actions", "spells_list"]} initialValue={initialSpells}>
        {(fields, { add, remove }) => (
          <>
            {fields.map(({ key, name, ...restField }) => (
              <SpellItem
                key={key}
                name={name}
                restField={restField}
                remove={remove}
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
