import { Card, Col, Row, Typography } from "antd";
/**
 * A component to display character attribute modifiers
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @returns {React.ReactElement}
 */
export default function AttributeModifiers({ character }) {
  const { Title, Text } = Typography;

  return (
    <Card title="Attribute Modifiers" style={{ marginBottom: 16 }}>
      <Row gutter={[16, 16]}>
        {Object.keys(character.attribute_modifiers).map((attribute) => (
          <Col xs={12} sm={8} md={4} key={attribute}>
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
                }}
              >
                {attribute.toUpperCase()}
              </Text>
              <Title level={4}>
                {character.attribute_modifiers[attribute] > 0
                  ? `+ ${character.attribute_modifiers[attribute]}`
                  : character.attribute_modifiers[attribute]}
              </Title>
            </div>
          </Col>
        ))}
      </Row>
    </Card>
  );
}
