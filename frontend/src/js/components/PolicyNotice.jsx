import { Typography } from "antd";

/**
 * A component to display Paizo's Community Use Policy Notice.
 *
 * This notice is required by Paizo for any content using Paizo material under
 * the Paizo Community Use Policy.
 *
 * @returns {React.ReactElement}
 */
export default function PolicyNotice() {
  const { Title, Text } = Typography;

  return (
    <>
      <Title>Community use Policy Notice</Title>
      <Text>
        <strong>Trailmarker</strong> uses trademarks and/or copyrights owned by
        Paizo Inc., used under Paizo&apos;s Community Use Policy (
        <a
          href="https://paizo.com/licenses/communityuse"
          target="_blank"
          rel="noreferrer"
          aria-label="Paizo Community Use Policy"
        >
          paizo.com/licenses/communityuse
        </a>
        ). We are expressly prohibited from charging you to use or access this
        content. <strong>Trailmarker</strong> is not published, endorsed, or
        specifically approved by Paizo. For more information about Paizo Inc.
        and Paizo products, visit{" "}
        <a
          href="https://paizo.com"
          target="_blank"
          rel="noreferrer"
          aria-label="Paizo Website"
        >
          paizo.com.
        </a>
      </Text>
    </>
  );
}
