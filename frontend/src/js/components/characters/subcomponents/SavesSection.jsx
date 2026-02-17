import { Card, Row, Col, Typography } from "antd";
import { toTitleCase } from "../../../services/helpers";

const { Title, Text } = Typography;

/**
 * A component to display character saving throws
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @returns {JSX.element}
 */
export default function SavesSection({ character }) {
  return (
    <Card title="Saving Throws" style={{ marginBottom: 16 }}>
      <Row gutter={[16, 16]} justify="space-evenly">
        {Object.keys(character.defenses.saves).map((save) => (
          <Col xs={24} sm={8} md={4} key={save}>
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
                {toTitleCase(save)}
              </Text>
              <Title level={4}>{character.defenses.saves[save]}</Title>
            </div>
          </Col>
        ))}
      </Row>
    </Card>
  );
}
