import { useContext } from "react";
import { Button, Form, Grid, Input, Typography } from "antd";

import { AuthContext } from "../../contexts/AuthContext.jsx";

/**
 * The page for the user to log into their account
 *
 * @returns {React.ReactElement}
 */
export default function Login() {
  const { login } = useContext(AuthContext);
  const screens = Grid.useBreakpoint();

  const { Title } = Typography;

  function handleSubmit(values) {
    login(values.username, values.password);
  }

  return (
    <>
      <Title>Login</Title>
      <Form
        name="login"
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
        <Form.Item label={null}>
          <Button type="primary" htmlType="submit">
            Login
          </Button>
        </Form.Item>
      </Form>
    </>
  );
}
