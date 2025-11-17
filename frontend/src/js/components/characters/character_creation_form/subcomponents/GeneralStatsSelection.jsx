import { Form, InputNumber, Select } from "antd";

export default function GeneralStatsSelection() {
  return (
    <>
      <Form.Item
        label="Level"
        name="level"
        rules={[{ required: true, message: "Please input a level" }]}
      >
        <Select
          style={{ width: 100 }}
          options={[
            {
              value: 1,
              label: "1",
            },
            {
              value: 2,
              label: "2",
            },
            {
              value: 3,
              label: "3",
            },
          ]}
        />
      </Form.Item>
      <Form.Item
        label="Hit Point Maximum"
        name="max_hit_points"
        rules={[
          { required: true, message: "Please input a hit point maximum value" },
        ]}
      >
        <InputNumber min={0} max={100} />
      </Form.Item>
      <Form.Item
        label="Armor Class"
        name={["defenses", "armor_class"]}
        rules={[
          { required: true, message: "Please input an armor class value" },
        ]}
      >
        <InputNumber min={0} max={30} />
      </Form.Item>
      <Form.Item
        label="Speed"
        name="speed"
        rules={[{ required: true, message: "Please input a speed value" }]}
      >
        <InputNumber min={0} max={50} />
      </Form.Item>
      <Form.Item
        label="Perception"
        name="perception"
        rules={[{ required: true, message: "Please input a perception value" }]}
      >
        <InputNumber min={-10} max={20} />
      </Form.Item>
    </>
  );
}
