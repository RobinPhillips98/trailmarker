import { Card, Row, Col, Typography, Empty } from "antd";
import { EllipsisOutlined } from "@ant-design/icons";
import { toTitleCase } from "../../../../services/helpers";

const { Title, Text } = Typography;

/**
 * A component to display the character header with name, player, and level
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @returns {JSX.element}
 */
export default function CharacterHeader({ character }) {
  return (
    <Card style={{ marginBottom: 16 }}>
      <Row gutter={[24, 16]}>
        <Col xs={24} sm={12} md={8}>
          <div>
            <Text
              strong
              style={{
                fontSize: "12px",
                display: "block",
                marginBottom: 4,
              }}
            >
              NAME
            </Text>
            <Title level={2} style={{ marginTop: 4 }}>
              {toTitleCase(character.name)}
            </Title>
          </div>
        </Col>
        <Col xs={24} sm={12} md={8}>
          <div>
            <Text
              strong
              style={{
                fontSize: "12px",
                display: "block",
                marginBottom: 4,
              }}
            >
              PLAYER
            </Text>
            <Title level={4} style={{ marginTop: 4 }}>
              {character.player ? character.player : <EllipsisOutlined />}
            </Title>
          </div>
        </Col>
        <Col xs={24} sm={12} md={8}>
          <div>
            <Text
              strong
              style={{
                fontSize: "12px",
                display: "block",
                marginBottom: 4,
              }}
            >
              LEVEL
            </Text>
            <Title level={4} style={{ marginTop: 4 }}>
              {character.level}
            </Title>
          </div>
        </Col>
      </Row>
    </Card>
  );
}
