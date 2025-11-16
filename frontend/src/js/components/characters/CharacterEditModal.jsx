import { useState } from "react";
import { Button, Modal } from "antd";
import CharacterCreationForm from "./CharacterCreationForm";
export default function CharacterEditModal({ character }) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  function showModal() {
    setIsModalOpen(true);
  }

  function handleCancel() {
    setIsModalOpen(false);
  };

  return (
    <>
      <Button type="primary" onClick={showModal}>
        Edit Character
      </Button>
      <Modal
        title="Edit Character"
        closable={{ "aria-label": "Custom Close Button" }}
        open={isModalOpen}
        footer={
          <Button key="back" onClick={handleCancel}>
            Cancel
          </Button>}
      >
        <CharacterCreationForm savedCharacter={character} editing={true} />
      </Modal>
    </>
  );
}
