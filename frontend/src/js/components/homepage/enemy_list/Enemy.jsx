import { Button, Card, Tag, Space, Typography } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { isEmpty } from "../../../services/helpers";

/**
 * A component to display an enemy that can be added to the encounter
 *
 * @param {object} props
 * @param {function} props.handleAdd The function to add the given enemy to the encounter
 * @param {object} props.enemy The enemy to be displayed
 * @returns {JSX.Element}
 */
export default function Enemy({ handleAdd, enemy }) {
  const { Text } = Typography;

  function handleClick() {
    handleAdd(enemy);
  }

  return (
    <Card
      hoverable
      style={{
        height: "100%",
        width: "100%",
        display: "flex",
        flexDirection: "column",
      }}
      styles={{
        body: {
          flex: 1,
          display: "flex",
          flexDirection: "column",
          padding: "16px",
          minHeight: 0,
        },
      }}
    >
      <div
        style={{
          flex: 1,
          minHeight: 0,
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Text
          strong
          style={{
            fontSize: "16px",
            display: "block",
            marginBottom: 12,
            whiteSpace: "nowrap",
          }}
          title={enemy.name}
        >
          {enemy.name}
        </Text>

        <div
          style={{
            flex: 1,
            minHeight: 0,
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
          }}
        >
          <Space
            direction="vertical"
            size="small"
            style={{ width: "100%", flex: 1 }}
          >
            <div>
              <Text type="secondary" style={{ fontSize: "12px" }}>
                Level
              </Text>
              <div style={{ fontSize: "18px", fontWeight: "bold" }}>
                {enemy.level}
              </div>
            </div>

            <div style={{ minHeight: 0, flex: 1 }}>
              <Text
                type="secondary"
                style={{ fontSize: "12px", display: "block" }}
              >
                Traits
              </Text>
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
                {enemy.traits.map((trait) => (
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
            {(enemy.immunities === undefined || enemy.immunities.length == 0) ? null : (
              <div style={{ minHeight: 0, flex: 1 }}>
                <Text
                  type="secondary"
                  style={{ fontSize: "12px", display: "block" }}
                >
                  Immunities
                </Text>
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
                  {enemy.immunities.map((immunity) => (
                    <Tag
                      key={immunity}
                      color="blue"
                      style={{
                        margin: 0,
                        maxWidth: "100%",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                      }}
                    >
                      {immunity}
                    </Tag>
                  ))}
                </div>
              </div>
            )}
            {(isEmpty(enemy.weaknesses)) ? null : (
              <div style={{ minHeight: 0, flex: 1 }}>
                <Text
                  type="secondary"
                  style={{ fontSize: "12px", display: "block" }}
                >
                  Weaknesses
                </Text>
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
                  {Object.keys(enemy.weaknesses).map((weakness) => (
                    <Tag
                      key={weakness}
                      color="blue"
                      style={{
                        margin: 0,
                        maxWidth: "100%",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                      }}
                    >
                      {weakness} : {enemy.weaknesses[weakness]}
                    </Tag>
                  ))}
                </div>
              </div>
            )}
            {(isEmpty(enemy.resistances)) ? null : (
              <div style={{ minHeight: 0, flex: 1 }}>
                <Text
                  type="secondary"
                  style={{ fontSize: "12px", display: "block" }}
                >
                  Resistances
                </Text>
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
                  {Object.keys(enemy.resistances).map((resistance) => (
                    <Tag
                      key={resistance}
                      color="blue"
                      style={{
                        margin: 0,
                        maxWidth: "100%",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                      }}
                    >
                      {resistance} : {enemy.resistances[resistance]}
                    </Tag>
                  ))}
                </div>
              </div>
            )}
          </Space>
        </div>
      </div>

      <Button
        type="primary"
        icon={<PlusOutlined />}
        onClick={handleClick}
        block
        style={{ marginTop: 12, flexShrink: 0 }}
      >
        Add
      </Button>
    </Card>
  );
}
