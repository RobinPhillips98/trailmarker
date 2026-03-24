import { Divider, Tabs, Typography } from "antd";

export default function GenericCharacters() {
  const { Text, Title } = Typography;
  const path = "/assets";
  const sheets = [`Cleric`, `Fighter`, `Rogue`, `Wizard`];

  const tabs = sheets.map((sheet) => ({
    key: sheet,
    label: sheet,
    children: (
      <iframe
        src={`${path}/${sheet}.pdf`}
        height={1000}
        width="100%"
        title={`${sheet} Character Sheet`}
      ></iframe>
    ),
  }));

  return (
    <>
      <Title>Generic Character Sheets</Title>
      <Text>
        Note: Some wording may be different as these character sheets come from
        Paizo&apos;s <em>Community Use Package</em> and use the legacy rules,
        while Trailmarker uses the remaster rules.
      </Text>
      <Divider />
      <Tabs type="card" size="large" items={tabs} />
    </>
  );
}
