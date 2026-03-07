import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { App, Button, Form, Grid, Input, Typography } from "antd";

import { AuthContext } from "../../contexts/AuthContext";

/**
 * The page to allow the user to register a new account
 *
 * @returns {React.ReactElement}
 */
export default function Register() {
  const { register, user } = useContext(AuthContext);
  const navigate = useNavigate();
  const screens = Grid.useBreakpoint();
  const { message } = App.useApp();

  function handleSubmit(values) {
    register(values.username, values.password);
  }

  const { Title } = Typography;

  useEffect(() => {
    if (user) {
      navigate("/");
      message.warning(
        "You are currently logged in. Please log out before registering.",
      );
    }
  }, [user, navigate]);

  return (
    <>
      <Title>Registration</Title>
      <Form
        name="register"
        onFinish={handleSubmit}
        labelCol={{
          span: screens.sm ? 8 : 24,
        }}
        wrapperCol={{
          span: screens.sm ? 16 : 24,
        }}
        style={{ maxWidth: 600 }}
        scrollToFirstError={{ focus: true }}
      >
        <Form.Item
          label="Username"
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
          <Button type="primary" htmlType="submit">
            Register
          </Button>
        </Form.Item>
      </Form>
    </>
  );
}
