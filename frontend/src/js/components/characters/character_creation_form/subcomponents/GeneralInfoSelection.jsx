import { Card, Form, Input, InputNumber, Select } from "antd";

import { ancestries, backgrounds, classes } from "../../characterHelpers";

/**
 * A component to allow a user to set general information about a player
 * character, such as their name, player name, and class
 *
 * @returns {JSX.element}
 */
export default function GeneralInfoSelection() {
  return (
    <Card style={{ height: 350, width: 300, marginLeft: 100 }}>
      <Form.Item
        label="Name"
        name="name"
        labelCol={{ span: 24 }}
        wrapperCol={{ span: 24 }}
        rules={[{ required: true, message: "Please input a character name" }]}
      >
        <Input />
      </Form.Item>
      <Form.Item
        label="Player Name"
        name="player"
        labelCol={{ span: 24 }}
        wrapperCol={{ span: 24 }}
      >
        <Input />
      </Form.Item>
      <Form.Item label="XP" name="xp">
        <InputNumber min={0} max={1000} />
      </Form.Item>
      <Form.Item
        label="Ancestry"
        name="ancestry"
        rules={[{ required: true, message: "Please select an ancestry" }]}
      >
        <Select options={ancestries} />
      </Form.Item>
      <Form.Item
        label="Background"
        name="background"
        rules={[{ required: true, message: "Please select a background" }]}
      >
        <Select options={backgrounds} />
      </Form.Item>
      <Form.Item
        label="Class"
        name="class"
        rules={[{ required: true, message: "Please select a class" }]}
      >
        <Select options={classes} />
      </Form.Item>
    </Card>
  );
}
