import api from "../../api";
import { useContext, useEffect } from "react";
import { AuthContext } from "../../contexts/AuthContext";
import { Button, Form} from "antd";
import { useNavigate } from "react-router-dom";
import AttributeSelection from "./subcomponents/AttributeSelection";
import SkillSelection from "./subcomponents/SkillSelection";
import SavesSelection from "./subcomponents/SavesSelection";
import AttacksSelection from "./subcomponents/AttacksSelection";
import GeneralInfoSelection from "./subcomponents/GeneralInfoSelection";
import GeneralStatsSelection from "./subcomponents/GeneralStatsSelection";

export default function CharacterCreationForm({ savedCharacter, editing }) {
  const { token } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      alert("Sorry: You must be logged in to access this page");
      navigate("/login");
    }
  }, [token, navigate]);

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
      <GeneralInfoSelection />
      <GeneralStatsSelection />
      <AttributeSelection editing={editing} savedCharacter={savedCharacter} />
      <br />
      <SkillSelection editing={editing} savedCharacter={savedCharacter} />
      <br />
      <SavesSelection />
      <br />
      <AttacksSelection editing={editing} savedCharacter={savedCharacter} />
      <br />
      <Form.Item label={null}>
        <Button type="primary" htmlType="submit">
          Save Character
        </Button>
      </Form.Item>
    </Form>
  );
}
