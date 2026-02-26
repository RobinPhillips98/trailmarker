import { Typography } from "antd";
import { Link } from "react-router-dom";

export default function PolicyNotice() {
  const { Title, Text } = Typography;

  return (
    <>
      <Title>Community use Policy Notice</Title>
      <Text>
        <strong>Trailmarker</strong> uses trademarks and/or copyrights owned by
        Paizo Inc., used under Paizo&apos;s Community Use Policy (
        <Link to="https://paizo.com/licenses/communityuse">
          paizo.com/licenses/communityuse
        </Link>
        ). We are expressly prohibited from charging you to use or access this
        content. <strong>Trailmarker</strong> is not published, endorsed, or
        specifically approved by Paizo. For more information about Paizo Inc.
        and Paizo products, visit <Link to="https://paizo.com">paizo.com.</Link>
      </Text>
    </>
  );
}
