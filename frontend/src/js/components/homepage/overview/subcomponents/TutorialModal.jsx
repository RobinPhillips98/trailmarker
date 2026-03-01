import { useState } from "react";
import { Button, FloatButton, Modal } from "antd";
import { QuestionCircleOutlined } from "@ant-design/icons";

/**
 * A component that displays a tutorial modal with a floating button.
 *
 * @returns {React.ReactElement}
 */
export default function TutorialModal() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  function showModal() {
    setIsModalOpen(true);
  }

  function closeModal() {
    setIsModalOpen(false);
  }

  return (
    <>
      <FloatButton
        type="primary"
        onClick={showModal}
        icon={<QuestionCircleOutlined />}
        tooltip="How To Use"
      />
      <Modal
        title="How To Enable Trailmarker's Simulation"
        closable={{ "aria-label": "Custom Close Button" }}
        open={isModalOpen}
        footer={[
          <Button key="ok" onClick={closeModal} type="primary">
            OK
          </Button>,
        ]}
      >
        <ol>
          <li>Register an account and login</li>
          <li>
            Navigate to &quot;Saved Characters&quot; then &quot;Create
            Character&quot; and fill out the character creation form for each
            character in your party.
          </li>
          <li>
            Return to the homepage and choose enemies using the list and filters
            below
          </li>
          <li>Run the simulation!</li>
        </ol>
      </Modal>
    </>
  );
}
