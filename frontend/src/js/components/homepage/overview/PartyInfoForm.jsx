import { Select, Typography } from "antd";
const { Title } = Typography;

const sizeOptions = [
  {
    value: "2",
    label: "2 Players",
  },
  {
    value: "3",
    label: "3 Players",
  },
  {
    value: "4",
    label: "4 Players",
  },
  {
    value: "5",
    label: "5 Players",
  },
  {
    value: "6",
    label: "6 Players",
  },
];

const levelOptions = [
  {
    value: "1",
    label: "1",
  },
  {
    value: "2",
    label: "2",
  },
  {
    value: "3",
    label: "3",
  },
];

function PartyInfoForm({ handlePartySize, handlePartyLevel }) {
  return (
    <div id="#partyInfoForm">
      <Title level={4}>Number of Players</Title>
      <Select
        defaultValue="4"
        options={sizeOptions}
        onChange={handlePartySize}
      />
      <Title level={4}>Party Level</Title>
      <Select
        defaultValue="1"
        options={levelOptions}
        onChange={handlePartyLevel}
      />
    </div>
  );
}

export default PartyInfoForm;
