import { Card, Form, InputNumber } from "antd";
import { skills, toTitleCase } from "../characterHelpers";

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
