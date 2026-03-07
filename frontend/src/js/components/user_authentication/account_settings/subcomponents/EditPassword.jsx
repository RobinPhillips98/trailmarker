// Third-party libraries
import { useContext } from "react";
import { Button, Form, Grid, Input } from "antd";
import { UserSwitchOutlined } from "@ant-design/icons";

// Personal Helpers
import useErrorMessage from "../../../../services/hooks/useErrorMessage";
import api from "../../../../api";

// Contexts
import { AuthContext } from "../../../../contexts/AuthContext";

/**
 * A component allowing a user to change their username.
 *
 * @returns {React.ReactElement}
 */
export default function EditPassword() {
  const screens = Grid.useBreakpoint();
  const { token, logoutWithRedirect } = useContext(AuthContext);
  const { errorMessage } = useErrorMessage();

  async function handleSubmit(values) {
    try {
      await api.patch("/users/", values, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      logoutWithRedirect(
        "/login",
        "Password updated successfully. Please login again",
      );
    } catch (error) {
      errorMessage("Error updating password", error);
    }
  }

  return (
    <>
      <Form
        name="EditPassword"
        labelCol={{
          span: screens.sm ? 8 : 24,
        }}
        wrapperCol={{
          span: screens.sm ? 16 : 24,
        }}
        style={{ maxWidth: 600 }}
        scrollToFirstError={{ focus: true }}
        onFinish={handleSubmit}
      >
        <Form.Item
          label="Enter Old Password"
          name="old_password"
          rules={[
            {
              required: true,
              message: "Please input your old password!",
            },
          ]}
        >
          <Input.Password />
        </Form.Item>
        <Form.Item
          label="New Password"
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
          label="Confirm New Password"
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
            htmlType="submit"
            icon={<UserSwitchOutlined />}
          >
            Change Password
          </Button>
        </Form.Item>
      </Form>
    </>
  );
}
