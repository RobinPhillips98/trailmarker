import { Card, Col, Row, Typography } from "antd";

import { toTitleCase } from "../../../../services/helpers";

/**
 * A component to display basic character info such as ancestry and class
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @returns {React.ReactElement}
 */
export default function CharacterBasics({ character }) {
  const { Text } = Typography;

  return (
    <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
      <Col xs={24} sm={12} md={6}>
        <Card title="Ancestry" size="small">
          <Text>
            {toTitleCase(character.heritage)} {toTitleCase(character.ancestry)}
          </Text>
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
