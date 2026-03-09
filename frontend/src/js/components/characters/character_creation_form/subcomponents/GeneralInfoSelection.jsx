import { useEffect, useState } from "react";
import { Card, Form, Input, Select, Tooltip, Typography } from "antd";
import { QuestionCircleOutlined } from "@ant-design/icons";

import {
  ancestries,
  backgrounds,
  classes,
  dwarfHeritages,
  elfHeritages,
  humanHeritages,
  otherFeatures,
} from "../../characterHelpers";

/**
 * A component to allow a user to set general information about a player
 * character, such as their name, player name, ancestry, heritage, and class
 *
 * @param {object} props
 * @param {object} props.form The ant design form instance.
 * @returns {React.ReactElement}
 */
export default function GeneralInfoSelection({ form }) {
  const ancestry = Form.useWatch("ancestry", form);
  const [heritages, setHeritages] = useState({});

  const { Text } = Typography;

  useEffect(() => {
    switch (ancestry) {
      case "dwarf":
        setHeritages(dwarfHeritages);
        break;
      case "elf":
        setHeritages(elfHeritages);
        break;
      case "human":
        setHeritages(humanHeritages);
        break;
      default:
        setHeritages({});
    }
  }, [ancestry]);

  const otherFeaturesLabel = (
    <>
      <Text style={{ marginRight: 5 }}>Other Features</Text>
      <Tooltip title="Features that may be used by the simulation but don't fit elsewhere">
        <QuestionCircleOutlined />
      </Tooltip>
    </>
  );

  return (
    <Card style={{ width: "100%" }}>
      <Form.Item
        label="Name"
        name="name"
        rules={[{ required: true, message: "Please input a character name" }]}
      >
        <Input />
      </Form.Item>
      <Form.Item label="Player Name" name="player">
        <Input />
      </Form.Item>
      <Form.Item
        label="Ancestry"
        name="ancestry"
        rules={[{ required: true, message: "Please select an ancestry" }]}
      >
        <Select
          value={ancestry}
          options={ancestries}
          style={{ width: "100%" }}
        />
      </Form.Item>
      <Form.Item
        label="Heritage"
        name="heritage"
        rules={[{ required: true, message: "Please select a heritage" }]}
      >
        <Select options={heritages} style={{ width: "100%" }} />
      </Form.Item>
      <Form.Item
        label="Background"
        name="background"
        rules={[{ required: true, message: "Please select a background" }]}
      >
        <Select options={backgrounds} style={{ width: "100%" }} />
      </Form.Item>
      <Form.Item
        label="Class"
        name="class"
        rules={[{ required: true, message: "Please select a class" }]}
      >
        <Select options={classes} style={{ width: "100%" }} />
      </Form.Item>
      <Form.Item label={otherFeaturesLabel} name="other_features">
        <Select options={otherFeatures} mode="multiple" allowClear />
      </Form.Item>
    </Card>
  );
}
