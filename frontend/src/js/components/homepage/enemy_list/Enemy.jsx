import { Button, Card, Space, Tag, Typography } from "antd";
import { MinusOutlined, PlusOutlined } from "@ant-design/icons";

import { isEmpty, MAX_ENEMY_QUANTITY } from "../../../services/helpers";

/**
 * A component to display an enemy that can be added to the encounter
 *
 * @typedef {object} EnemyProps
 * @property {function} props.handleAdd The function to add the given enemy to the
 *  encounter
 * @property {function} props.handleDecrement The function to decrement the
 *  quantity of the given enemy
 * @property {object} props.enemy The enemy to be displayed
 *
 * @param {EnemyProps} props
 * @returns {React.ReactElement}
 */
export default function Enemy(props) {
  const { handleAdd, handleDecrement, enemy } = props;
  const { Text } = Typography;

  function handleClickAdd() {
    handleAdd(enemy);
  }

  function handleClickDecrement() {
    handleDecrement(enemy);
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
              <Text strong style={{ fontSize: "12px" }}>
                Level
              </Text>
              <div style={{ fontSize: "18px", fontWeight: "bold" }}>
                {enemy.level}
              </div>
            </div>

            <div style={{ minHeight: 0, flex: 1 }}>
              <Text strong style={{ fontSize: "12px", display: "block" }}>
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

            {enemy.immunities?.length > 0 && (
              <div style={{ minHeight: 0, flex: 1 }}>
                <Text strong style={{ fontSize: "12px", display: "block" }}>
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

            {!isEmpty(enemy.weaknesses) && (
              <div style={{ minHeight: 0, flex: 1 }}>
                <Text strong style={{ fontSize: "12px", display: "block" }}>
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

            {!isEmpty(enemy.resistances) && (
              <div style={{ minHeight: 0, flex: 1 }}>
                <Text strong style={{ fontSize: "12px", display: "block" }}>
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
        onClick={handleClickAdd}
        block
        disabled={enemy.quantity >= MAX_ENEMY_QUANTITY}
      >
        Add {enemy.quantity ? `(${enemy.quantity})` : null}
      </Button>
      <Button
        type="primary"
        danger
        icon={<MinusOutlined />}
        onClick={handleClickDecrement}
        block
        disabled={!enemy.quantity}
        style={{ marginTop: 12 }}
      >
        Remove
      </Button>
    </Card>
  );
}
