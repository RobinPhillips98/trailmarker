import { Card, Col, Row, Typography } from "antd";

/**
 * A component to display core character stats such as hit points or speed.
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @returns {React.ReactElement}
 */
export default function CoreStats({ character }) {
  const { Title } = Typography;

  const armorClassDisplay =
    character.actions?.shield > 0
      ? `${character.defenses.armor_class} + 🛡${character.actions.shield}`
      : character.defenses.armor_class;

  return (
    <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
      <Col xs={24} sm={12} md={6}>
        <Card title="Maximum Hit Points" size="small">
          <div style={{ textAlign: "center" }}>
            <Title level={3}>{character.max_hit_points}</Title>
          </div>
        </Card>
      </Col>

      <Col xs={24} sm={12} md={6}>
        <Card title="Armor Class" size="small">
          <div style={{ textAlign: "center" }}>
            <Title level={3}>{armorClassDisplay}</Title>
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
