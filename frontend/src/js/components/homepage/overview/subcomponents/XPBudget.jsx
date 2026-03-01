import { Card, Space, Switch, Tag, Typography } from "antd";

/**
 * A component to display the XP budget for the current party size
 *
 * @typedef {object} XPBudgetProps
 * @property {object} budget The XP budget for the current party size
 * @property {boolean} switched State of the colorblind switch
 * @property {function} handleChange The function for handling when the color
 *  blind friendly switch is switched
 * @property {object} colors The currently set difficulty colors
 *
 * @param {XPBudgetProps} props
 * @returns {React.ReactElement}
 */
export default function XPBudget(props) {
  const { budget, switched, handleChange, colors } = props;
  const { Title, Text } = Typography;

  const budgetTiers = [
    { label: "Trivial", xp: budget.trivial, color: colors.trivial },
    { label: "Low", xp: budget.low, color: colors.low },
    { label: "Moderate", xp: budget.moderate, color: colors.moderate },
    { label: "Severe", xp: budget.severe, color: colors.severe },
    { label: "Extreme", xp: budget.extreme, color: colors.extreme },
  ];

  return (
    <Card style={{ height: "100%" }}>
      <Title level={4} style={{ marginTop: 0 }}>
        XP Budget
      </Title>
      <Space direction="vertical" style={{ width: "100%" }} size={12}>
        {budgetTiers.map((tier) => (
          <div
            key={tier.label}
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: "8px",
            }}
          >
            <Tag color={tier.color} style={{ fontSize: "14px", margin: 0 }}>
              {tier.label}
            </Tag>
            <Text strong style={{ fontSize: "18px" }}>
              {tier.xp} XP
            </Text>
          </div>
        ))}
        <Title level={5} style={{ marginBottom: 8 }}>
          Colorblind friendly?
        </Title>
        <Switch checked={switched} onChange={handleChange} />
      </Space>
    </Card>
  );
}
