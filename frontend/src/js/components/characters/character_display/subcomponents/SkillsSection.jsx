import { Card, Col, Row, Typography } from "antd";

import { toTitleCase } from "../../../../services/helpers";

/**
 * A component to display character skills
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @returns {React.ReactElement}
 */
export default function SkillsSection({ character }) {
  const { Title, Text } = Typography;

  return (
    <Card title="Skills" style={{ marginBottom: 16 }}>
      <Row gutter={[16, 16]} justify="center">
        {Object.keys(character.skills).map((skill) => (
          <Col xs={12} sm={8} key={skill}>
            <div
              style={{
                textAlign: "center",
                padding: "8px",
                border: "1px solid #d9d9d9",
                borderRadius: "4px",
              }}
            >
              <Text
                strong
                style={{
                  fontSize: "12px",
                  display: "block",
                  marginBottom: 4,
                  textTransform: "uppercase",
                }}
              >
                {toTitleCase(skill)}
              </Text>
              <Title level={4}>{character.skills[skill]}</Title>
            </div>
          </Col>
        ))}
      </Row>
    </Card>
  );
}
