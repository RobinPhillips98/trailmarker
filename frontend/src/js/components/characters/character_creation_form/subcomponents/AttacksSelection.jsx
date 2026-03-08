import { Card, Form, Select } from "antd";
import {} from "@ant-design/icons";

import { weaponOptions, weaponTypeOptions } from "../../characterHelpers";

/**
 * A component to allow a user to add attacks to a player character
 *
 * @param {object} props
 * @param {boolean} props.editing True if this is a saved character being
 *  edited, false if this is a new character.
 * @param {object} props.savedCharacter The character being edited, if any.
 * @returns {React.ReactElement}
 */
export default function AttacksSelection() {
  return (
    <Card title="Attacks" style={{ width: "100%" }}>
      <Form.Item name={["actions", "attacks"]} label="Weapons">
        <Select options={weaponOptions} allowClear mode="multiple" />
      </Form.Item>
      <Form.Item name={"trained"} label="Trained Weapon Proficiencies">
        <Select options={weaponTypeOptions} allowClear mode="multiple" />
      </Form.Item>
      <Form.Item name={"expert"} label="Expert Weapon Proficiencies">
        <Select options={weaponTypeOptions} allowClear mode="multiple" />
      </Form.Item>
      <Form.Item name={"extra_trained"} label="Extra Trained Proficiencies">
        <Select options={weaponOptions} allowClear mode="multiple" />
      </Form.Item>
      <Form.Item name={"extra_expert"} label="Extra Expert Proficiencies">
        <Select options={weaponOptions} allowClear mode="multiple" />
      </Form.Item>
    </Card>
  );
}
