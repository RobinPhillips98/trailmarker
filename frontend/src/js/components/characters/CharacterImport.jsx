// Third-party libraries
import { useContext, useState } from "react";
import { App, Button, Modal, Space, Upload } from "antd";
import {
  MenuOutlined,
  QuestionCircleOutlined,
  UploadOutlined,
} from "@ant-design/icons";

// Personal helpers
import api from "../../api";
import useErrorMessage from "../../services/hooks/useErrorMessage";

// Contexts
import { AuthContext } from "../../contexts/AuthContext";

/**
 * A component to display a button to allow users to upload a character.
 *
 * @param {object} props
 * @param {function} props.addCharacter The function to add a character to the
 *  display
 * @returns {React.ReactElement}
 */
export default function CharacterImport({ addCharacter }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [warningOpen, setWarningOpen] = useState(false);

  const { message } = App.useApp();
  const { token } = useContext(AuthContext);
  const { errorMessage } = useErrorMessage();

  function showModal() {
    setIsModalOpen(true);
  }

  function handleOk() {
    setIsModalOpen(false);
  }

  function handleCancel() {
    setIsModalOpen(false);
  }

  /**
   * Function to handle upload of a file to import a Pathbuilder character.
   *
   * @param {File} file The character being uploaded
   * @returns {boolean}
   */
  function handleUpload(file) {
    const isJson =
      file.type === "application/json" || file.name.endsWith(".json");
    if (!isJson) {
      message.error("Invalid File: Please upload a JSON file.");
      return false;
    }
    const reader = new FileReader();

    reader.onload = async () => {
      try {
        const parsed_file = JSON.parse(reader.result);
        const character = parsed_file.build;
        if (!character) {
          message.error(
            "Invalid file: not a Pathbuilder JSON export (no build object found).",
          );
          return;
        }
        const response = await api.post("/characters/import", character, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        addCharacter(response.data);
        message.success("Character imported successfully!");
        if (!warningOpen) {
          setWarningOpen(true);
          message.warning(
            "Please note the import is not always perfect. Some values may have to be manually adjusted.",
            7.5,
            () => setWarningOpen(false),
          );
        }
      } catch (error) {
        errorMessage("Error importing character", error);
        if (error?.status === 422)
          message.warning(
            "Build object exists, but could not be processed due to formatting issues.",
            7.5,
          );
      }
    };

    reader.onerror = () => {
      message.error("Failed to read file.");
    };

    reader.readAsText(file);

    // Return false to stop Ant Design's built in upload function
    return false;
  }

  const uploadProps = {
    name: "file",
    accept: ".json",
    maxCount: 1,
    showUploadList: false,
    beforeUpload: handleUpload,
  };

  return (
    <Space>
      <Upload {...uploadProps}>
        <Button icon={<UploadOutlined />}>Upload Pathbuilder JSON</Button>
      </Upload>
      <Button
        type="primary"
        onClick={showModal}
        shape="circle"
        icon={<QuestionCircleOutlined />}
        size="small"
      />
      <Modal
        title="Exporting Pathbuilder Characters"
        closable={{ "aria-label": "Custom Close Button" }}
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <ol>
          <li>
            Create a character at{" "}
            <a href="https://pathbuilder2e.com">pathbuilder2e.com</a>
          </li>
          <li>
            Click <MenuOutlined /> Menu to open the menu, then click
            &quot;Export JSON&quot;
          </li>
          <li>Click &quot;View JSON&quot;</li>
          <li>
            Press Ctrl + S or right click and select &quot;Save Page As&quot;,
            choose a name for the file, and save the file.
          </li>
          <li>
            Return here, click the &quot;Upload Pathbuilder JSON&quot; button,
            browse to the file you&apos;ve just saved and upload it.
          </li>
        </ol>
        <p>Note: Pathbuilder2e is not affiliated with Trailmarker</p>
      </Modal>
    </Space>
  );
}
