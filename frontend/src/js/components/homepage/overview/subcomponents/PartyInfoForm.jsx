// Third-party libraries
import { useContext } from "react";
import { Card, Form, Select, Space, Switch } from "antd";
import { CheckOutlined, CloseOutlined } from "@ant-design/icons";

// Personal helpers
import { levelOptions } from "../../../../services/helpers";

// Contexts
import { AuthContext } from "../../../../contexts/AuthContext";

/**
 * A component to allow users to enter information about their party
 *
 * @typedef {object} PartyInfoFormProps
 * @property {number} partySize The number of characters in the party
 * @property {number} partyLevel The level of the characters in the party
 * @property {boolean} switched Whether the "use saved characters" switch is
 *  toggled
 * @property {boolean} charactersSaved Whether the user has any characters
 *  already saved.
 * @property {function} handlePartySize The function to set the party size
 *  based on the select component
 * @property {function} handlePartyLevel The function to set the party level
 *  based on the select component
 * @property {function} handleChange The function to handle when the switch is
 *  toggled
 *
 * @param {PartyInfoFormProps} props
 * @returns {React.ReactElement}
 */
export default function PartyInfoForm(props) {
  const {
    partySize,
    partyLevel,
    switched,
    charactersSaved,
    handlePartySize,
    handlePartyLevel,
    handleChange,
  } = props;

  const { user } = useContext(AuthContext);

  const disabled = !user || !charactersSaved;

  const sizeOptions = [
    {
      value: "1",
      label: 1,
    },
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

  return (
    <Card title="Difficulty Calculation Options" style={{ height: "100%" }}>
      <Space direction="vertical" style={{ width: "100%" }} size="large">
        <Form labelCol={{ span: 24 }} wrapperCol={{ span: 24 }}>
          <Form.Item label="Use Saved Characters?">
            <Switch
              checked={switched}
              onChange={handleChange}
              disabled={disabled}
              checkedChildren={<CheckOutlined />}
              unCheckedChildren={<CloseOutlined />}
            />
          </Form.Item>
          <Form.Item label="Number of Players">
            <Select
              defaultValue="2"
              value={partySize}
              options={sizeOptions}
              onChange={handlePartySize}
              disabled={switched}
              style={{ width: "100%" }}
            />
          </Form.Item>
          <Form.Item label="Party Level">
            <Select
              defaultValue="1"
              value={partyLevel}
              options={levelOptions}
              onChange={handlePartyLevel}
              disabled={switched}
              style={{ width: "100%" }}
            />
          </Form.Item>
        </Form>
      </Space>
    </Card>
  );
}
