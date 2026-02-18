import { Card, Row, Col, Typography } from "antd";
import { toTitleCase } from "../../../../services/helpers";

const { Text } = Typography;

/**
 * A component to display character basics (ancestry, background, class, xp)
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @returns {JSX.element}
 */
export default function CharacterBasics({ character }) {
  return (
    <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
      <Col xs={24} sm={12} md={6}>
        <Card title="Ancestry" size="small">
          <Text>{toTitleCase(character.ancestry)}</Text>
        </Card>
      </Col>
      <Col xs={24} sm={12} md={6}>
        <Card title="Background" size="small">
          <Text>{toTitleCase(character.background)}</Text>
        </Card>
      </Col>
      <Col xs={24} sm={12} md={6}>
        <Card title="Class" size="small">
          <Text>{toTitleCase(character.class)}</Text>
        </Card>
      </Col>
      <Col xs={24} sm={12} md={6}>
        <Card title="XP" size="small">
          <Text>{character.xp}</Text>
        </Card>
      </Col>
    </Row>
  );
}
