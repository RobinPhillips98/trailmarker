import { Card, Col, Divider, Empty, List, Row, Typography } from "antd";

import { toTitleCase, splitCamelCase } from "../../../../services/helpers";

/**
 * A component to display character spellcasting information, if any
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @returns {React.ReactElement}
 */
export default function SpellcastingSection({ character }) {
  const { Text, Title } = Typography;

  const hasSpells =
    character.actions?.spells && character.actions.spells.length > 0;

  const hasHeals = character.actions?.heals > 0;

  if (!hasSpells && !hasHeals) return null;

  return (
    <>
      <Divider style={{ marginTop: 32, marginBottom: 16 }} />
      <Title level={3} style={{ marginBottom: 16 }}>
        Spellcasting
      </Title>

      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col xs={24} sm={12} md={6}>
          <Card title="Spell Attack Bonus" size="small">
            <div style={{ textAlign: "center" }}>
              <Title level={4}>
                {character.spell_attack_bonus || (
                  <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} />
                )}
              </Title>
            </div>
          </Card>
        </Col>

        <Col xs={24} sm={12} md={6}>
          <Card title="Spell DC" size="small">
            <div style={{ textAlign: "center" }}>
              <Title level={4}>
                {character.spell_dc || (
                  <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} />
                )}
              </Title>
            </div>
          </Card>
        </Col>

        {hasHeals && (
          <Col xs={24} sm={12} md={6}>
            <Card title="Heal Spells Prepared" size="small">
              <div style={{ textAlign: "center" }}>
                <Title level={4}>{character.actions.heals}</Title>
              </div>
            </Card>
          </Col>
        )}
      </Row>

      {hasSpells && (
        <Card title="Spells">
          <Row gutter={[16, 16]}>
            {character.actions.spells.map((spell) => (
              <Col xs={24} sm={12} md={8} key={spell.name}>
                <Card
                  title={toTitleCase(spell.name)}
                  size="small"
                  style={{ height: "100%" }}
                >
                  <List size="small">
                    <List.Item>
                      <Text strong>Level:</Text>{" "}
                      {spell.level > 0 ? spell.level : "Cantrip"}
                    </List.Item>

                    {spell.slots && spell.level > 0 && (
                      <List.Item>
                        <Text strong>Slots:</Text> {spell.slots}
                      </List.Item>
                    )}

                    <List.Item>
                      <Text strong>Damage:</Text> {spell.damage_roll}
                    </List.Item>

                    <List.Item>
                      <Text strong>Type:</Text> {toTitleCase(spell.damage_type)}
                    </List.Item>

                    <List.Item>
                      <Text strong>Range:</Text> {spell.range}
                    </List.Item>

                    <List.Item>
                      <Text strong>Target:</Text> {spell.target}
                    </List.Item>

                    <List.Item>
                      <Text strong>Actions:</Text> {spell.actions}
                    </List.Item>

                    {spell.save && (
                      <List.Item>
                        <Text strong>Save:</Text> {toTitleCase(spell.save)}
                      </List.Item>
                    )}

                    {spell.area &&
                      typeof spell.area === "object" &&
                      Object.keys(spell.area).map((key) => (
                        <List.Item key={key}>
                          <Text strong>
                            Area {toTitleCase(splitCamelCase(key))}:
                          </Text>{" "}
                          {spell.area[key]}
                        </List.Item>
                      ))}
                  </List>
                </Card>
              </Col>
            ))}
          </Row>
        </Card>
      )}
    </>
  );
}
