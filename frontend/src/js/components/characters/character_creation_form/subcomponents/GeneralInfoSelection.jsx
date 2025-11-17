import { Form, Input, InputNumber, Select } from "antd";
import { ancestries, backgrounds, classes } from "../characterHelpers";

export default function GeneralInfoSelection() {
  return (
    <>
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
    </>
  );
}
