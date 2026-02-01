import { useContext } from "react";
import { Select, Switch, Typography } from "antd";

import { AuthContext } from "../../../contexts/AuthContext";

/**
 * A component to allow users to enter information about their party
 *
 * @typedef {object} PartyInfoFormProps
 * @property {number} partySize The number of characters in the party
 * @property {number} partyLevel The level of the characters in the party
 * @property {boolean} switched Whether the "use saved characters" switch is toggled
 * @property {function} handlePartySize The function to set the party size based on the select component
 * @property {function} handlePartyLevel The function to set the party level based on the select component
 * @property {function} handleChange The function to handle when the switch is toggled
 *
 * @param {PartyInfoFormProps} props
 * @returns {JSX.Element}
 */
export default function PartyInfoForm(props) {
  const {
    partySize,
    partyLevel,
    switched,
    handlePartySize,
    handlePartyLevel,
    handleChange,
  } = props;

  const { Title } = Typography;
  const { user } = useContext(AuthContext);

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

  return (
    <div id="#partyInfoForm">
      <Title level={2}>Use saved characters?</Title>
      <Switch checked={switched} onChange={handleChange} disabled={!user} />
      <Title level={2}>Number of Players</Title>
      <Select
        defaultValue="2"
        value={partySize}
        options={sizeOptions}
        onChange={handlePartySize}
        disabled={switched}
      />
      <Title level={2}>Party Level</Title>
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
