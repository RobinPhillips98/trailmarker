import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Form, Input } from "antd";

import { AuthContext } from "../contexts/AuthContext";

/**
 * The page to allow the user to register a new account
 *
 * @returns {JSX.Element}
 */
export default function Register() {
  const { register, user } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      alert("You already logged in. Please log out before registering");
      navigate("/");
    }
  }, [user, navigate]);

  function handleSubmit(values) {
    register(values.username, values.password);
  }

  return (
    <Form
      name="register"
      onFinish={handleSubmit}
      labelCol={{ span: 8 }}
      wrapperCol={{ span: 16 }}
      style={{ maxWidth: 600 }}
      scrollToFirstError={{ focus: true }}
    >
      <Form.Item
        label="Username"
        name="username"
        rules={[{ required: true, message: "Please input your username!" }]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        label="Password"
        name="password"
        rules={[{ required: true, message: "Please input your password!" }]}
      >
        <Input.Password />
      </Form.Item>
      <Form.Item label={null}>
        <Button type="primary" htmlType="submit">
          Register
        </Button>
      </Form.Item>
    </Form>
  );
}
