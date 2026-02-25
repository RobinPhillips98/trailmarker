import { Card, Form, InputNumber, Select } from "antd";

/**
 * A component to allow a user to set general numerical stats for a player
 * character, such as their level, hit point maximum, or armor class
 *
 * @returns {JSX.element}
 */
export default function GeneralStatsSelection() {
  return (
    <Card style={{ width: "100%" }}>
      <Form.Item
        label="Level"
        labelCol={{ span: 12 }}
        name="level"
        rules={[{ required: true, message: "Please input a level" }]}
        style={{ marginTop: 20 }}
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
      <Form.Item label="XP" labelCol={{ span: 12 }} name="xp">
        <InputNumber min={0} max={1000} style={{ width: 120 }} />
      </Form.Item>
      <Form.Item
        label="Hit Point Maximum"
        labelCol={{ span: 12 }}
        name="max_hit_points"
        rules={[
          { required: true, message: "Please input a hit point maximum value" },
        ]}
      >
        <InputNumber min={0} max={100} />
      </Form.Item>
      <Form.Item
        label="Spell Attack Bonus"
        labelCol={{ span: 12 }}
        name="spell_attack_bonus"
      >
        <InputNumber min={0} max={20} style={{ width: 120 }} />
      </Form.Item>
      <Form.Item label="Spell DC" labelCol={{ span: 12 }} name="spell_dc">
        <InputNumber min={0} max={30} style={{ width: 120 }} />
      </Form.Item>
      <Form.Item
        label="Armor Class"
        labelCol={{ span: 12 }}
        name={["defenses", "armor_class"]}
        rules={[
          { required: true, message: "Please input an armor class value" },
        ]}
      >
        <InputNumber min={0} max={30} />
      </Form.Item>
      <Form.Item
        label="Shield Value"
        labelCol={{ span: 12 }}
        name={["actions", "shield"]}
      >
        <InputNumber min={0} max={5} />
      </Form.Item>
      <Form.Item
        label="Speed"
        labelCol={{ span: 12 }}
        name="speed"
        rules={[{ required: true, message: "Please input a speed value" }]}
      >
        <InputNumber min={0} max={50} />
      </Form.Item>
      <Form.Item
        label="Perception"
        labelCol={{ span: 12 }}
        name="perception"
        rules={[{ required: true, message: "Please input a perception value" }]}
      >
        <InputNumber min={-10} max={20} />
      </Form.Item>
      <Form.Item
        label="Heals Prepared"
        labelCol={{ span: 12 }}
        name={["actions", "heals"]}
      >
        <InputNumber min={0} max={5} />
      </Form.Item>
    </Card>
  );
}
