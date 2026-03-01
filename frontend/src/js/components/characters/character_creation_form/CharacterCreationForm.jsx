import { useContext, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  Button,
  Col,
  Form,
  Row,
  Grid,
  Typography,
  Space,
  FloatButton,
} from "antd";
import { CloseOutlined, SaveOutlined } from "@ant-design/icons";

import AttributeSelection from "./subcomponents/AttributeSelection";
import SkillSelection from "./subcomponents/SkillSelection";
import SavesSelection from "./subcomponents/SavesSelection";
import AttacksSelection from "./subcomponents/AttacksSelection";
import GeneralInfoSelection from "./subcomponents/GeneralInfoSelection";
import GeneralStatsSelection from "./subcomponents/GeneralStatsSelection";
import SpellsSelection from "./subcomponents/SpellsSelection";

import api from "../../../api";
import { AuthContext } from "../../../contexts/AuthContext";
import { errorAlert } from "../../../services/helpers";

/**
 * A component to allow a user to create or edit a player character
 *
 * @returns {React.ReactElement}
 */
export default function CharacterCreationForm() {
  const { state } = useLocation();
  const { editing, savedCharacter } = state;
  const { token } = useContext(AuthContext);
  const { useBreakpoint } = Grid;
  const navigate = useNavigate();
  const { Title } = Typography;

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
        heritage: savedCharacter.heritage,
        background: savedCharacter.background,
        class: savedCharacter.class,
        level: savedCharacter.level,
        max_hit_points: savedCharacter.max_hit_points,
        spell_attack_bonus: savedCharacter.spell_attack_bonus,
        spell_dc: savedCharacter.spell_dc,
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
          attacks: savedCharacter.actions?.attacks,
          spells: savedCharacter.actions?.spells,
          heals: savedCharacter.actions?.heals,
          shield: savedCharacter.actions?.shield,
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

  /**
   * Attempts to save the current character to the database, either patching an
   * existing character or posting a new character
   *
   * @param {object} character The character to be saved
   */
  async function onFinish(character) {
    try {
      if (editing) {
        character.id = savedCharacter.id;
        await api.patch("/characters", character, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
      } else {
        await api.post("/characters", character, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
      }
      navigate("/characters", {
        state: { selectedCharacter: character.name },
      });
    } catch (error) {
      errorAlert("Error saving character", error);
    }
  }

  function handleCancel() {
    navigate("/characters");
  }

  const title = editing ? "Edit Character" : "Character Creation";

  const formSize = useBreakpoint().lg ? "large" : "middle";

  return (
    <>
      <Title>{title}</Title>
      <Form
        name="character"
        labelCol={{ span: 24 }}
        wrapperCol={{ span: 24 }}
        style={{ maxWidth: 1200, margin: "0 auto" }}
        initialValues={initialValues}
        onFinish={onFinish}
        autoComplete="off"
        size={formSize}
        requiredMark="optional"
        scrollToFirstError={{ focus: true }}
      >
        <Space style={{ marginTop: 24, marginBottom: 24 }}>
          <Form.Item label={null}>
            <Button type="primary" htmlType="submit" icon={<SaveOutlined />}>
              Save Character
            </Button>
          </Form.Item>
          <Form.Item label={null}>
            <Button onClick={handleCancel} icon={<CloseOutlined />}>
              Cancel
            </Button>
          </Form.Item>
        </Space>
        <FloatButton.Group shape="square">
          <FloatButton
            type="primary"
            htmlType="submit"
            icon={<SaveOutlined />}
            tooltip="Save Character"
          />
          <FloatButton
            onClick={handleCancel}
            icon={<CloseOutlined />}
            tooltip="Cancel"
          />
          <FloatButton.BackTop />
        </FloatButton.Group>
        <Row gutter={16} align="middle">
          <Col xs={24} md={12}>
            <GeneralInfoSelection
              editing={editing}
              savedCharacter={savedCharacter}
            />
          </Col>
          <Col xs={24} md={12}>
            <GeneralStatsSelection />
          </Col>
        </Row>
        <br />
        <Row gutter={16} align="middle">
          <Col xs={24} md={12}>
            <AttributeSelection
              editing={editing}
              savedCharacter={savedCharacter}
            />
          </Col>
          <Col xs={24} md={12}>
            <SavesSelection />
          </Col>
        </Row>
        <br />
        <Row>
          <Col span={24}>
            <SkillSelection editing={editing} savedCharacter={savedCharacter} />
          </Col>
        </Row>
        <br />
        <Row gutter={16}>
          <Col xs={24} md={12}>
            <AttacksSelection
              editing={editing}
              savedCharacter={savedCharacter}
            />
          </Col>
          <Col xs={24} md={12}>
            <SpellsSelection
              editing={editing}
              savedCharacter={savedCharacter}
            />
          </Col>
        </Row>
        <br />
      </Form>
    </>
  );
}
