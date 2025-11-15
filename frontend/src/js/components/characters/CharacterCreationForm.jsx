import api from "../../api";
import { useContext } from "react";
import { AuthContext } from "../../contexts/AuthContext";
import { MinusOutlined, PlusOutlined } from "@ant-design/icons";
import { Button, Card, Form, Input, InputNumber, Select, Space } from "antd";
import {
  ancestries,
  backgrounds,
  classes,
  attributes,
  skills,
  saves,
} from "./characterData";
import { useNavigate } from "react-router-dom";

export default function CharacterCreationForm() {
  const { token } = useContext(AuthContext);
  const navigate = useNavigate();

  const [form] = Form.useForm();

  async function onFinish(character) {
    await api.post("/characters", character, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    navigate("/characters");
  }

  return (
    <Form
      name="basic"
      form={form}
      labelCol={{ span: 8 }}
      wrapperCol={{ span: 16 }}
      style={{ maxWidth: 600 }}
      initialValues={{ level: "1", variant: "filled" }}
      onFinish={onFinish}
      autoComplete="off"
      size="small"
      requiredMark="optional"
    >
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
        <InputNumber />
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
      <Form.Item
        label="Level"
        name="level"
        rules={[{ required: true, message: "Please input a level" }]}
      >
        <Select
          style={{ width: 100 }}
          options={[
            {
              value: "1",
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
        <InputNumber />
      </Form.Item>
      <Form.Item
        label="Armor Class"
        name={["defenses", "armor_class"]}
        rules={[
          { required: true, message: "Please input an armor class value" },
        ]}
      >
        <InputNumber />
      </Form.Item>
      <Form.Item
        label="Speed"
        name="speed"
        rules={[{ required: true, message: "Please input a speed value" }]}
      >
        <InputNumber />
      </Form.Item>
      <Form.Item
        label="Perception"
        name="perception"
        rules={[{ required: true, message: "Please input a perception value" }]}
      >
        <InputNumber />
      </Form.Item>

      <Card
        title="Attribute Modifiers"
        size="small"
        style={{ marginLeft: 100, width: 300 }}
        variant="borderless"
      >
        {attributes.map((attribute) => (
          <Form.Item
            label={attribute}
            name={["attribute_modifiers", attribute.toLowerCase()]}
            rules={[
              {
                required: true,
                message: `Please input a ${attribute.toLowerCase()} value`,
              },
            ]}
          >
            <InputNumber />
          </Form.Item>
        ))}
      </Card>
      <br />
      <Card
        title="Skills"
        size="small"
        style={{ marginLeft: 100, width: 300 }}
        variant="borderless"
      >
        {skills.map((skill) => (
          <Form.Item
            label={skill}
            name={["skills", skill.toLowerCase()]}
            rules={[
              {
                required: true,
                message: `Please input a ${skill.toLowerCase()} value`,
              },
            ]}
          >
            <InputNumber />
          </Form.Item>
        ))}
      </Card>
      <br />
      <Card
        title="Saving Throws"
        size="small"
        style={{ marginLeft: 100, width: 300 }}
        variant="borderless"
      >
        {saves.map((save) => (
          <Form.Item
            label={save}
            name={["defenses", "saves", save.toLowerCase()]}
            rules={[
              {
                required: true,
                message: `Please input a ${save.toLowerCase()} value`,
              },
            ]}
          >
            <InputNumber />
          </Form.Item>
        ))}
      </Card>
      <br />
      <Card
        title="Attacks"
        size="small"
        style={{ marginLeft: 100, width: 300 }}
        variant="borderless"
      >
        <Form.List name={["actions", "attacks"]}>
          {(fields, { add, remove }) => (
            <>
              {fields.map(({ name, ...restField }) => (
                <Card>
                  <Form.Item
                    {...restField}
                    name={[name, "name"]}
                    label="Name"
                    rules={[{ required: true, message: "Please input a name" }]}
                  >
                    <Input />
                  </Form.Item>
                  <Form.Item
                    {...restField}
                    name={[name, "attackBonus"]}
                    label="Attack Bonus"
                    rules={[
                      {
                        required: true,
                        message: "Please input an attack bonus",
                      },
                    ]}
                  >
                    <InputNumber />
                  </Form.Item>
                  <Form.Item
                    {...restField}
                    name={[name, "damage"]}
                    label="Damage"
                    rules={[
                      { required: true, message: "Please input a damage" },
                    ]}
                  >
                    <Input placeholder="1d8+4" />
                  </Form.Item>
                  <Form.Item
                    {...restField}
                    name={[name, "damageType"]}
                    label="DamageType"
                    rules={[
                      { required: true, message: "Please input a damageType" },
                    ]}
                  >
                    <Input placeholder="Slashing" />
                  </Form.Item>
                  <Button
                    type="dashed"
                    icon={<MinusOutlined />}
                    onClick={() => remove(name)}
                  >
                    Remove Attack
                  </Button>
                </Card>
              ))}
              <br />
              <Form.Item>
                <Button
                  type="dashed"
                  onClick={() => add()}
                  block
                  icon={<PlusOutlined />}
                >
                  Add attack
                </Button>
              </Form.Item>
            </>
          )}
        </Form.List>
      </Card>
      <br />
      <Form.Item label={null}>
        <Button type="primary" htmlType="submit">
          Create Character
        </Button>
      </Form.Item>
    </Form>
  );
}
