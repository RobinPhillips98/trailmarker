import api from "../../api";
import { useContext, useEffect } from "react";
import { AuthContext } from "../../contexts/AuthContext";
import { MinusOutlined, PlusOutlined } from "@ant-design/icons";
import { Button, Card, Form, Input, InputNumber, Select } from "antd";
import {
  ancestries,
  backgrounds,
  classes,
  damageTypes,
  attributes,
  skills,
  saves,
  toTitleCase,
} from "./characterHelpers";
import { useNavigate } from "react-router-dom";

export default function CharacterCreationForm({ savedCharacter, editing }) {
  const { token, user } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token || !user) {
      alert("Sorry: You must be logged in to access this page");
      navigate("/login");
    }
  }, [token, user, navigate]);

  const initialValues = editing
    ? {
        name: savedCharacter.name,
        player: savedCharacter.player,
        xp: savedCharacter.xp,
        ancestry: savedCharacter.ancestry,
        background: savedCharacter.background,
        class: savedCharacter.class,
        level: savedCharacter.level,
        max_hit_points: savedCharacter.max_hit_points,
        defenses: {
          armor_class: savedCharacter.defenses.armor_class,
          saves: {
            fortitude: savedCharacter.defenses.saves.fortitude,
            reflex: savedCharacter.defenses.saves.reflex,
            will: savedCharacter.defenses.saves.will,
          },
        },
        speed: savedCharacter.speed,
        perception: savedCharacter.perception,
        actions: {
          attacks: savedCharacter.attacks,
        },
      }
    : {
        level: "1",
        max_hit_points: 0,
        defenses: {
          armor_class: 0,
          saves: {
            fortitude: 0,
            reflex: 0,
            will: 0,
          },
        },
        speed: 0,
        perception: 0,
      };

  async function onFinish(character) {
    try {
      if (editing) {
        character.id = savedCharacter.id;
        await api.patch("/characters", character, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        window.location.reload();
      } else {
        await api.post("/characters", character, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        navigate("/characters");
      }
    } catch (error) {
      alert(error.response.data.detail);
    }
  }

  const initialAttacks = editing
    ? savedCharacter.actions.attacks.map((attack) => ({
        name: attack.name,
        attackBonus: attack.attackBonus,
        damage: attack.damage,
        damageType: attack.damageType,
      }))
    : [{}];

  return (
    <Form
      name="character"
      labelCol={{ span: 8 }}
      wrapperCol={{ span: 16 }}
      style={{ maxWidth: 600 }}
      initialValues={initialValues}
      onFinish={onFinish}
      autoComplete="off"
      size="small"
      requiredMark="optional"
      scrollToFirstError={{ focus: true }}
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

      <Card
        title="Attribute Modifiers"
        size="small"
        style={{ marginLeft: 100, width: 300 }}
        variant="borderless"
      >
        {attributes.map((attribute) => (
          <Form.Item
            label={toTitleCase(attribute)}
            name={["attribute_modifiers", attribute]}
            initialValue={
              editing ? savedCharacter.attribute_modifiers[attribute] : 0
            }
            rules={[
              {
                required: true,
                message: `Please input a ${attribute} value`,
              },
            ]}
          >
            <InputNumber min={-2} max={5} />
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
            label={toTitleCase(skill)}
            name={["skills", skill]}
            initialValue={editing ? savedCharacter.skills[skill] : 0}
            rules={[
              {
                required: true,
                message: `Please input a ${skill} value`,
              },
            ]}
          >
            <InputNumber min={-10} max={30} />
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
            label={toTitleCase(save)}
            name={["defenses", "saves", save]}
            rules={[
              {
                required: true,
                message: `Please input a ${save} value`,
              },
            ]}
          >
            <InputNumber min={-5} max={30} />
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
        <Form.List name={["actions", "attacks"]} initialValue={initialAttacks}>
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
                    <InputNumber min={-5} max={30} />
                  </Form.Item>
                  <Form.Item
                    {...restField}
                    name={[name, "damage"]}
                    label="Damage"
                    rules={[
                      { required: true, message: "Please input a damage" },
                      {
                        pattern: /^\dd(4|6|8|10|12)([+-]\d\d?)?$/i,
                        message:
                          "Damage must be in the form #d# or #d#±# (ex. 1d4 or 1d8+4)",
                      },
                    ]}
                  >
                    <Input placeholder="1d8+4" />
                  </Form.Item>
                  <Form.Item
                    {...restField}
                    name={[name, "damageType"]}
                    label="Damage Type"
                    rules={[
                      { required: true, message: "Please input a damage type" },
                    ]}
                  >
                    <Select options={damageTypes} />
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
          Save Character
        </Button>
      </Form.Item>
    </Form>
  );
}
