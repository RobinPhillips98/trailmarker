import { Card, Form, Input, Select } from "antd";

import {
  ancestries,
  backgrounds,
  classes,
  dwarfHeritages,
  elfHeritages,
  humanHeritages,
} from "../../characterHelpers";
import { useEffect, useState } from "react";

/**
 * A component to allow a user to set general information about a player
 * character, such as their name, player name, and class
 *
 * @returns {JSX.element}
 */
export default function GeneralInfoSelection({ savedCharacter }) {
  const [ancestry, setAncestry] = useState(savedCharacter?.ancestry);
  const [heritages, setHeritages] = useState({});

  function handleChangeAncestry(newAncestry) {
    setAncestry(newAncestry);
  }

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
          onChange={handleChangeAncestry}
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
    </Card>
  );
}
