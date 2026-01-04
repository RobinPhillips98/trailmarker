import { Card, Form, InputNumber } from "antd";

import { skills } from "../../characterHelpers";
import { toTitleCase } from "../../../../services/helpers";

/**
 * A component to allow a user to set a player character's skills
 *
 * @param {object} props
 * @param {boolean} props.editing True if this is a saved character being edited, false if this is a new character
 * @param {object} props.savedCharacter The character being edited
 * @returns {JSX.element}
 */
export default function SkillSelection({ editing, savedCharacter }) {
  return (
    <Card
      key="skills"
      title="Skills"
      size="small"
      style={{ marginLeft: 100, width: 300 }}
      variant="borderless"
    >
      {skills.map((skill) => (
        <Form.Item
          key={skill}
          label={toTitleCase(skill)}
          name={["skills", skill]}
          initialValue={editing ? savedCharacter.skills[skill] : 0}
          rules={[
            {
              required: true,
              message: `Please input a ${skill} value`,
            },
          ]}
        >
          <InputNumber min={-10} max={30} />
        </Form.Item>
      ))}
    </Card>
  );
}
