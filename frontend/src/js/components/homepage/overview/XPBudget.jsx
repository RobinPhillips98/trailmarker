import { List, Typography } from "antd";

/**
 * A component to display the XP budget for the current party size
 *
 * @param {object} props
 * @param {object} props.budget The XP budget for the current party size
 * @returns {JSX.Element}
 */
export default function XPBudget({ budget }) {
  const { Title } = Typography;

  const budgetDisplay = [
    `Trivial: ${budget.trivial} XP`,
    `Low: ${budget.low} XP`,
    `Moderate: ${budget.moderate} XP`,
    `Severe: ${budget.severe} XP`,
    `Extreme: ${budget.extreme} XP`,
  ];
  return (
    <List
      header={<Title level={5}>XP Budget</Title>}
      size="small"
      dataSource={budgetDisplay}
      renderItem={(item) => <List.Item>{item}</List.Item>}
      bordered={true}
    />
  );
}
