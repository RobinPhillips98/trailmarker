import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Modal, Space, Typography } from "antd";
import { DeleteOutlined, EditOutlined } from "@ant-design/icons";

/**
 * A component displaying controls for editing and deleting a character
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @param {function} props.deleteCharacter Function to delete a character
 * @returns {React.ReactElement}
 */
export default function CharacterControls({ character, deleteCharacter }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();
  const { Title } = Typography;

  function showModal() {
    setIsModalOpen(true);
  }

  function closeModal() {
    setIsModalOpen(false);
  }

  function handleDelete() {
    deleteCharacter(character);
  }

  function handleEdit() {
    navigate("/characters/create", {
      state: { editing: true, savedCharacter: character },
    });
  }

  return (
    <Space style={{ marginTop: 24, marginBottom: 24 }}>
      <Button type="primary" onClick={handleEdit} icon={<EditOutlined />}>
        Edit Character
      </Button>

      <Button
        type="primary"
        danger
        onClick={showModal}
        icon={<DeleteOutlined />}
      >
        Delete Character
      </Button>
      <Modal
        closable={{ "aria-label": "Custom Close Button" }}
        open={isModalOpen}
        onCancel={closeModal}
        footer={[
          <Button key="cancel" onClick={closeModal}>
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
  );
}
