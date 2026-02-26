import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Modal, Typography, Space } from "antd";
import { DeleteOutlined, EditOutlined } from "@ant-design/icons";

export default function CharacterControls({ character, deleteCharacter }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { Title } = Typography;
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
  );
}
