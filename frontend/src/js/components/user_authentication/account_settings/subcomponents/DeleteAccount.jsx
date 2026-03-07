// Third-party libraries
import { useContext, useState } from "react";
import { Button, Form, Grid, Input, Modal, Typography } from "antd";
import { DeleteOutlined, UserDeleteOutlined } from "@ant-design/icons";

// Personal Helpers
import useErrorMessage from "../../../../services/hooks/useErrorMessage";
import api from "../../../../api";

// Contexts
import { AuthContext } from "../../../../contexts/AuthContext";

/**
 * A component allowing a user to delete their account.
 *
 * @returns {React.ReactElement}
 */
export default function DeleteAccount() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const screens = Grid.useBreakpoint();
  const { token, logoutWithRedirect } = useContext(AuthContext);
  const { errorMessage } = useErrorMessage();
  const { Title } = Typography;

  const [form] = Form.useForm();
  const password = Form.useWatch("password", form);

  function showModal() {
    setIsModalOpen(true);
  }

  function closeModal() {
    setIsModalOpen(false);
  }

  async function handleSubmit() {
    const request = {
      password: password,
    };
    try {
      await api.delete("/users/", {
        data: request,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      logoutWithRedirect("/", "Account deleted!");
    } catch (error) {
      errorMessage("Error deleting account", error);
    }
  }

  return (
    <>
      <Form
        name="DeleteAccount"
        labelCol={{
          span: screens.sm ? 8 : 24,
        }}
        wrapperCol={{
          span: screens.sm ? 16 : 24,
        }}
        style={{ maxWidth: 600 }}
        scrollToFirstError={{ focus: true }}
        onFinish={showModal}
        form={form}
      >
        <Form.Item
          label="Password"
          name="password"
          rules={[
            {
              required: true,
              message: "Please input your password!",
            },
          ]}
        >
          <Input.Password />
        </Form.Item>
        <Form.Item
          label="Confirm Password"
          name="confirm"
          dependencies={["password"]}
          rules={[
            {
              required: true,
              message: "Please confirm your password!",
            },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue("password") === value) {
                  return Promise.resolve();
                }
                return Promise.reject(new Error("Passwords do not match"));
              },
            }),
          ]}
        >
          <Input.Password />
        </Form.Item>
        <Form.Item label={null}>
          <Button
            type="primary"
            danger
            htmlType="submit"
            icon={<UserDeleteOutlined />}
          >
            Delete Account
          </Button>
        </Form.Item>
      </Form>
      <Modal
        closable={{ "aria-label": "Custom Close Button" }}
        open={isModalOpen}
        onCancel={closeModal}
        footer={[
          <Button key="cancel" onClick={closeModal}>
            Cancel
          </Button>,
          <Button
            key="confirm"
            type="primary"
            danger
            onClick={handleSubmit}
            icon={<DeleteOutlined />}
          >
            CONFIRM
          </Button>,
        ]}
      >
        <Title level={2}>Are you sure?</Title>
        <Title level={3}>This action is irreversible!</Title>
        <Title level={3}>Deleted accounts cannot be recovered!</Title>
        <Title level={3}>You will have to create a new account!</Title>
      </Modal>
    </>
  );
}
