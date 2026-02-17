import { Card, Row, Col, Typography } from "antd";

const { Title } = Typography;

/**
 * A component to display core character stats (HP, AC, speed, perception)
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @returns {JSX.element}
 */
export default function CoreStats({ character }) {
  return (
    <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
      <Col xs={24} sm={12} md={6}>
        <Card title="Hit Points" size="small">
          <div style={{ textAlign: "center" }}>
            <Title level={3}>{character.max_hit_points}</Title>
          </div>
        </Card>
      </Col>
      <Col xs={24} sm={12} md={6}>
        <Card title="Armor Class" size="small">
          <div style={{ textAlign: "center" }}>
            <Title level={3}>{character.defenses.armor_class}</Title>
          </div>
        </Card>
      </Col>
      <Col xs={24} sm={12} md={6}>
        <Card title="Speed" size="small">
          <div style={{ textAlign: "center" }}>
            <Title level={4}>{character.speed} ft.</Title>
          </div>
        </Card>
      </Col>
      <Col xs={24} sm={12} md={6}>
        <Card title="Perception" size="small">
          <div style={{ textAlign: "center" }}>
            <Title level={4}>{character.perception}</Title>
          </div>
        </Card>
      </Col>
    </Row>
  );
}
