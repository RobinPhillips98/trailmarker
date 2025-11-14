import { List } from "antd";

function XPBudget({ budget }) {
  const budgetDisplay = [
    `Trivial: ${budget.trivial} XP`,
    `Low: ${budget.low} XP`,
    `Moderate: ${budget.moderate} XP`,
    `Severe: ${budget.severe} XP`,
    `Extreme: ${budget.extreme} XP`,
  ];
  return (
    <List
      header={<strong>XP Budget</strong>}
      size="small"
      dataSource={budgetDisplay}
      renderItem={(item) => <List.Item>{item}</List.Item>}
      bordered={true}
    />
  );
}

export default XPBudget;
