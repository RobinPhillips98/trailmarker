import { useState } from "react";
import { Button, Collapse, FloatButton, Modal } from "antd";
import { MenuOutlined, QuestionCircleOutlined } from "@ant-design/icons";

/**
 * A component that displays a tutorial modal with a floating button.
 *
 * @param {object} props
 * @param {React.RefObject} props.ref The reference used by the opening tour to
 * target this component
 * @param {function} props.setTourOpen The function to set whether or not the
 *  opening tour is open.
 * @returns {React.ReactElement}
 */
export default function TutorialModal({ ref, setTourOpen }) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  function showModal() {
    setIsModalOpen(true);
  }

  function closeModal() {
    setIsModalOpen(false);
  }

  function handleClickTutorial() {
    closeModal();
    setTourOpen(true);
  }

  const items = [
    {
      key: "collapse_1",
      label: "Basic Usage",
      children: (
        <>
          <p>
            Select enemies from the list then press the &quot;Run
            Simulation&quot; button to run a simulation with pre-generated
            characters.
          </p>
          <p>
            Use the filters to search for certain enemies based on name, level,
            traits, immunities, and resistances.
          </p>
          <p>
            Other features, such as running a simulation with custom characters,
            require creating an account.
          </p>
        </>
      ),
    },
    {
      key: "collapse_2",
      label: "Saving Encounters",
      children: (
        <>
          <strong>You must have an account to save encounters.</strong>
          <p>
            To save an encounter, simply select the enemies you want then click
            &quot;Save Encounter&quot;
          </p>
          <p>
            Optionally, you may give the encounter a name using the textbox.
            Once the encounter is saved, you can click &quot;Open Saved
            Encounters&quot; to display your saved encounters and select one to
            use.
          </p>
        </>
      ),
    },
    {
      key: "collapse_3",
      label: "Creating Custom Characters",
      children: (
        <>
          <strong>You must have an account to create custom characters.</strong>
          <p>
            To create a character, use the navbar (or <MenuOutlined /> nav menu
            on mobile) and click on &quot;Saved Characters&quot; to open the
            character display page
          </p>
          <p>
            Once on the character display page, you can click &quot;Create
            Character&quot; to open the character creation form. Fill it out,
            click save, and your character will be ready to use in simulations!
          </p>
          <p>
            After creating characters, you can use the &quot;Edit
            Character&quot; button to change any values the character has, or
            &quot;Delete Character&quot; to delete the character
          </p>
          <p>
            Once you&apos;ve saved some characters, you can use those characters
            in the simulation, simply uncheck the &quot;Use pre-generated
            characters?&quot; switch.
          </p>
        </>
      ),
    },
  ];

  return (
    <>
      <FloatButton
        type="primary"
        onClick={showModal}
        icon={<QuestionCircleOutlined />}
        tooltip="How To Use"
        ref={ref}
      />
      <Modal
        title="How To Use Trailmarker"
        closable={{ "aria-label": "Custom Close Button" }}
        open={isModalOpen}
        onCancel={closeModal}
        footer={[
          <Button key="open_tour" onClick={handleClickTutorial}>
            View Tutorial
          </Button>,
          <Button key="ok" onClick={closeModal} type="primary">
            OK
          </Button>,
        ]}
      >
        <Collapse items={items} defaultActiveKey={["collapse_1"]} />
      </Modal>
    </>
  );
}
