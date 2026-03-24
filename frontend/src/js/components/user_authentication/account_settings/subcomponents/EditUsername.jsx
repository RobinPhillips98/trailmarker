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
export default function EditUsername() {
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
        "/users/login",
        "Username updated successfully. Please login again",
      );
    } catch (error) {
      errorMessage("Error updating username", error);
    }
  }

  return (
    <>
      <Form
        name="EditUsername"
        labelCol={{
          span: screens.sm ? 8 : 24,
        }}
        wrapperCol={{
          span: screens.sm ? 16 : 24,
        }}
        style={screens.xs ? { maxWidth: 400 } : { maxWidth: 600 }}
        scrollToFirstError={{ focus: true }}
        onFinish={handleSubmit}
      >
        <Form.Item
          label="New Username"
          name="username"
          rules={[
            {
              required: true,
              message: "Please input your username!",
            },
          ]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          label="Password"
          name="old_password"
          rules={[
            {
              required: true,
              message: "Please input your password!",
            },
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
            Change Username
          </Button>
        </Form.Item>
      </Form>
    </>
  );
}
