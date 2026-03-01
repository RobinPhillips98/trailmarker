import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Form, Grid, Input, Typography } from "antd";

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

  function handleSubmit(values) {
    register(values.username, values.password);
  }

  const { Title } = Typography;

  useEffect(() => {
    if (user) {
      alert("You are currently logged in. Please log out before registering");
      navigate("/");
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
        <Form.Item label={null}>
          <Button type="primary" htmlType="submit">
            Register
          </Button>
        </Form.Item>
      </Form>
    </>
  );
}
