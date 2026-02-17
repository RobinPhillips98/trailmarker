import { useState } from "react";
import { Button, Modal, Space, Typography } from "antd";
import { useNavigate } from "react-router-dom";

import CharacterHeader from "./subcomponents/CharacterHeader";
import CharacterBasics from "./subcomponents/CharacterBasics";
import CoreStats from "./subcomponents/CoreStats";
import AttributeModifiers from "./subcomponents/AttributeModifiers";
import SavesSection from "./subcomponents/SavesSection";
import SkillsSection from "./subcomponents/SkillsSection";
import AttacksSection from "./subcomponents/AttacksSection";
import SpellcastingSection from "./subcomponents/SpellcastingSection";

const { Title } = Typography;

/**
 * A component to display information about a given character
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @param {function} props.deleteCharacter The function to delete the displayed character
 * @returns {JSX.element}
 */
export default function CharacterDisplay({ character, deleteCharacter }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();

  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const handleDelete = () => {
    deleteCharacter(character);
  };

  const handleEdit = () => {
    navigate("/characters/create", {
      state: { editing: true, savedCharacter: character },
    });
  };

  return (
    <div>
      <CharacterHeader character={character} />
      <CharacterBasics character={character} />
      <CoreStats character={character} />
      <AttributeModifiers character={character} />
      <SavesSection character={character} />
      <SkillsSection character={character} />
      <AttacksSection character={character} />
      <SpellcastingSection character={character} />

      <Space style={{ marginTop: 24 }}>
        <Button type="primary" onClick={handleEdit}>
          Edit Character
        </Button>

        <Button type="primary" danger onClick={showModal}>
          Delete Character
        </Button>
        <Modal
          closable={{ "aria-label": "Custom Close Button" }}
          open={isModalOpen}
          onCancel={handleCancel}
          footer={[
            <Button key="cancel" onClick={handleCancel}>
              Cancel
            </Button>,
            <Button key="yes" type="primary" danger onClick={handleDelete}>
              Yes
            </Button>,
          ]}
        >
          <Title>Are you sure?</Title>
          <Title level={2}>This action is irreversible!</Title>
          <Title level={3}>Deleted characters cannot be recovered!</Title>
        </Modal>
      </Space>
    </div>
  );
}
