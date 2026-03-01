import { Card, Col, Form, InputNumber, Row } from "antd";

import { skills } from "../../characterHelpers";
import { toTitleCase } from "../../../../services/helpers";

/**
 * A component to allow a user to set a player character's skills
 *
 * @param {object} props
 * @param {boolean} props.editing True if this is a saved character being
 *  edited, false if this is a new character.
 * @param {object} props.savedCharacter The character being edited, if any.
 * @returns {React.ReactElement}
 */
export default function SkillSelection({ editing, savedCharacter }) {
  return (
    <Card key="skills" title="Skills" style={{ width: "100%" }}>
      <Row>
        <Col span={8}>
          {skills.slice(0, 6).map((skill) => (
            <Form.Item
              key={skill}
              label={toTitleCase(skill)}
              labelCol={{ span: 12 }}
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
        </Col>
        <Col span={8}>
          {skills.slice(6, 12).map((skill) => (
            <Form.Item
              key={skill}
              label={toTitleCase(skill)}
              labelCol={{ span: 12 }}
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
        </Col>
        <Col span={8}>
          {skills.slice(12, 17).map((skill) => (
            <Form.Item
              key={skill}
              label={toTitleCase(skill)}
              labelCol={{ span: 12 }}
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
        </Col>
      </Row>
    </Card>
  );
}
