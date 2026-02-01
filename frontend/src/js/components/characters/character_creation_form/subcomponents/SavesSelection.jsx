import { Card, Col, Form, InputNumber, Row } from "antd";

import { saves } from "../../characterHelpers";
import { toTitleCase } from "../../../../services/helpers";

/**
 * A component to allow a user to set a player character's saving throws
 *
 * @returns {JSX.element}
 */
export default function SavesSelection() {
  return (
    <Card title="Saving Throws" style={{ width: "100%" }}>
      <Row gutter={16}>
        {saves.map((save) => (
          <Col key={save} span={8}>
            <Form.Item
              label={toTitleCase(save)}
              labelCol={{ span: 24 }}
              name={["defenses", "saves", save]}
              rules={[
                {
                  required: true,
                  message: `Please input a ${save} value`,
                },
              ]}
            >
              <InputNumber min={-5} max={30} style={{ width: "100%" }} />
            </Form.Item>
          </Col>
        ))}
      </Row>
    </Card>
  );
}
