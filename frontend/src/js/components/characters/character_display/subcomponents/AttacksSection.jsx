import { Card, Row, Col, List, Tag } from "antd";
import { toTitleCase } from "../../../../services/helpers";

/**
 * A component to display character attacks
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @returns {JSX.element}
 */
export default function AttacksSection({ character }) {
  const attacks = character.actions?.attacks || [];
  if (attacks.length === 0) return null;

  return (
    <Card title="Attacks" style={{ marginBottom: 16 }}>
      <Row gutter={[16, 16]}>
        {attacks.map((attack) => (
          <Col xs={24} sm={12} md={8} key={attack.name}>
            <Card title={attack.name} size="small" style={{ height: "100%" }}>
              <List size="small">
                <List.Item>
                  <strong>Attack Bonus:</strong> {attack.attackBonus}
                </List.Item>
                <List.Item>
                  <strong>Damage:</strong> {attack.damage}
                </List.Item>
                <List.Item>
                  <strong>Type:</strong> {toTitleCase(attack.damageType)}
                </List.Item>
                <List.Item>
                  <strong>Range: </strong> {attack.range ? attack.range : "5"}{" "}
                  feet
                </List.Item>
                <List.Item>
                  {attack.traits ? (
                    <div style={{ minHeight: 0, flex: 1 }}>
                      <strong>Traits:</strong>
                      <div
                        style={{
                          marginTop: 4,
                          display: "flex",
                          flexWrap: "wrap",
                          gap: 4,
                          maxHeight: "100%",
                          overflow: "hidden",
                        }}
                      >
                        {attack.traits.map((trait) => (
                          <Tag
                            key={trait}
                            color="blue"
                            style={{
                              margin: 0,
                              maxWidth: "100%",
                              overflow: "hidden",
                              textOverflow: "ellipsis",
                            }}
                          >
                            {trait}
                          </Tag>
                        ))}
                      </div>
                    </div>
                  ) : null}
                </List.Item>
              </List>
            </Card>
          </Col>
        ))}
      </Row>
    </Card>
  );
}
