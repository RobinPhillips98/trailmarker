// Third-Party Libraries
import { useContext } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  App,
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

// Personal Helpers
import api from "../../../api";
import { isEmpty } from "../../../services/helpers";
import useErrorMessage from "../../../services/hooks/useErrorMessage";

// Contexts
import { AuthContext } from "../../../contexts/AuthContext";

// Components
import AttributeSelection from "./subcomponents/AttributeSelection";
import SkillSelection from "./subcomponents/SkillSelection";
import SavesSelection from "./subcomponents/SavesSelection";
import AttacksSelection from "./subcomponents/AttacksSelection";
import GeneralInfoSelection from "./subcomponents/GeneralInfoSelection";
import GeneralStatsSelection from "./subcomponents/GeneralStatsSelection";
import SpellsSelection from "./subcomponents/SpellsSelection";
import NotAuthorized from "../../status_pages/NotAuthorized";

/**
 * A component to allow a user to create or edit a player character
 *
 * @returns {React.ReactElement}
 */
export default function CharacterCreationForm() {
  const { message } = App.useApp();
  const { token } = useContext(AuthContext);
  const { state } = useLocation();
  const { editing, savedCharacter } = state || {
    editing: false,
    savedCharacter: null,
  };
  const navigate = useNavigate();
  const { Title } = Typography;
  const { errorMessage } = useErrorMessage();

  const [form] = Form.useForm();

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
          attacks: savedCharacter.actions?.attacks.map((attack) =>
            attack.name.toLowerCase(),
          ),
          spells: savedCharacter.actions?.spells,
          heals: savedCharacter.actions?.heals,
          shield: savedCharacter.actions?.shield,
        },
        trained: isEmpty(savedCharacter.proficiencies)
          ? []
          : Object.keys(savedCharacter.proficiencies).filter(
              (proficiency) => savedCharacter.proficiencies[proficiency] === 2,
            ),
        expert: isEmpty(savedCharacter.proficiencies)
          ? []
          : Object.keys(savedCharacter.proficiencies).filter(
              (proficiency) => savedCharacter.proficiencies[proficiency] === 4,
            ),
        extra_trained: isEmpty(savedCharacter.extra_proficiencies)
          ? []
          : Object.keys(savedCharacter.extra_proficiencies).filter(
              (proficiency) =>
                savedCharacter.extra_proficiencies[proficiency] === 2,
            ),
        extra_expert: isEmpty(savedCharacter.extra_proficiencies)
          ? []
          : Object.keys(savedCharacter.extra_proficiencies).filter(
              (proficiency) =>
                savedCharacter.extra_proficiencies[proficiency] === 4,
            ),
        other_features: savedCharacter.other_features,
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
      // Use form's spells_list to build object of spells and slots
      if (character.actions?.spells_list) {
        character.actions.spells = Object.fromEntries(
          character.actions.spells_list.map(({ key, slots }) => [key, slots]),
        );
        delete character.actions.spells_list;
      }
      // Set numerical proficiency values based on what user entered
      if (character.trained || character.expert) character.proficiencies = {};
      character.trained?.forEach(
        (proficiency) => (character.proficiencies[proficiency] = 2),
      );
      delete character.trained;

      character.expert?.forEach(
        (proficiency) => (character.proficiencies[proficiency] = 4),
      );
      delete character.expert;

      if (character.extra_trained || character.extra_expert)
        character.extra_proficiencies = {};
      character.extra_trained?.forEach(
        (proficiency) => (character.extra_proficiencies[proficiency] = 2),
      );
      delete character.extra_trained;

      character.extra_expert?.forEach(
        (proficiency) => (character.extra_proficiencies[proficiency] = 4),
      );
      delete character.extra_expert;

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
      message.success("Character saved!");
    } catch (error) {
      errorMessage("Error saving character", error);
    }
  }

  function handleCancel() {
    navigate("/characters");
  }

  const title = editing ? "Edit Character" : "Character Creation";

  const formSize = Grid.useBreakpoint().lg ? "large" : "middle";

  if (token)
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
          form={form}
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
              <GeneralStatsSelection form={form} />
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
              <SkillSelection
                editing={editing}
                savedCharacter={savedCharacter}
              />
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
  else return <NotAuthorized />;
}
