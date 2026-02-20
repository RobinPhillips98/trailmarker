import { Typography, Card, Space, Tag, Switch } from "antd";

/**
 * A component to display the XP budget for the current party size
 *
 * @param {object} props
 * @param {object} props.budget The XP budget for the current party size
 * @returns {JSX.Element}
 */
export default function XPBudget({ budget, switched, handleChange, colors }) {
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
