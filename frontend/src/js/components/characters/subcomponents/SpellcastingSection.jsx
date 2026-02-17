import { Card, Row, Col, Divider, List, Typography, Empty } from "antd";
import { toTitleCase, splitCamelCase } from "../../../services/helpers";

const { Title } = Typography;

/**
 * A component to display character spellcasting information
 * Only renders if the character has spells
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @returns {JSX.element}
 */
export default function SpellcastingSection({ character }) {
  const hasSpells =
    character.actions?.spells && character.actions.spells.length > 0;

  if (!hasSpells) return null;

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
      </Row>

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
                    <strong>Level:</strong>{" "}
                    {spell.level > 0 ? spell.level : "Cantrip"}
                  </List.Item>
                  {spell.slots && spell.level > 0 && (
                    <List.Item>
                      <strong>Slots:</strong> {spell.slots}
                    </List.Item>
                  )}
                  <List.Item>
                    <strong>Damage:</strong> {spell.damage_roll}
                  </List.Item>
                  <List.Item>
                    <strong>Type:</strong> {toTitleCase(spell.damage_type)}
                  </List.Item>
                  <List.Item>
                    <strong>Range:</strong> {spell.range}
                  </List.Item>
                  <List.Item>
                    <strong>Target:</strong> {spell.target}
                  </List.Item>
                  <List.Item>
                    <strong>Actions:</strong> {spell.actions}
                  </List.Item>
                  {spell.save && (
                    <List.Item>
                      <strong>Save:</strong> {toTitleCase(spell.save)}
                    </List.Item>
                  )}
                  {spell.area &&
                    typeof spell.area === "object" &&
                    Object.keys(spell.area).map((key) => (
                      <List.Item key={key}>
                        <strong>
                          Area {toTitleCase(splitCamelCase(key))}:
                        </strong>{" "}
                        {spell.area[key]}
                      </List.Item>
                    ))}
                </List>
              </Card>
            </Col>
          ))}
        </Row>
      </Card>
    </>
  );
}
