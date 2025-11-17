import { useState } from "react";
import { Button, Modal } from "antd";

import CharacterCreationForm from "./character_creation_form/CharacterCreationForm";

/**
 * A component to display a modal to edit a given character
 *
 * @param {object} props
 * @param {object} props.character The character being edited
 * @returns {JSX.element}
 */
export default function CharacterEditModal({ character }) {
  const [isOpen, setIsOpen] = useState(false);

  function openModal() {
    setIsOpen(true);
  }

  function closeModal() {
    setIsOpen(false);
  }

  return (
    <>
      <Button type="primary" onClick={openModal}>
        Edit Character
      </Button>
      <Modal
        title="Edit Character"
        closable={{ "aria-label": "Custom Close Button" }}
        onCancel={closeModal}
        open={isOpen}
        footer={
          <Button key="cancel" onClick={closeModal}>
            Cancel
          </Button>
        }
      >
        <CharacterCreationForm savedCharacter={character} editing={true} />
      </Modal>
    </>
  );
}
