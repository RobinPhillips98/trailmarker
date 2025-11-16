import { Select, Switch, Typography } from "antd";
import { useContext } from "react";
import { AuthContext } from "../../../contexts/AuthContext";
const { Title } = Typography;

const sizeOptions = [
  {
    value: "2",
    label: "2",
  },
  {
    value: "3",
    label: "3",
  },
  {
    value: "4",
    label: "4",
  },
  {
    value: "5",
    label: "5",
  },
  {
    value: "6",
    label: "6",
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

function PartyInfoForm({
  partySize,
  partyLevel,
  switched,
  handlePartySize,
  handlePartyLevel,
  handleChange,
}) {
  const { user } = useContext(AuthContext);

  return (
    <div id="#partyInfoForm">
      <Title level={4}>Use saved characters?</Title>
      <Switch checked={switched} onChange={handleChange} disabled={!user} />
      <Title level={4}>Number of Players</Title>
      <Select
        defaultValue="4"
        value={partySize}
        options={sizeOptions}
        onChange={handlePartySize}
        disabled={switched}
      />
      <Title level={4}>Party Level</Title>
      <Select
        defaultValue="1"
        value={partyLevel}
        options={levelOptions}
        onChange={handlePartyLevel}
        disabled={switched}
      />
    </div>
  );
}

export default PartyInfoForm;
