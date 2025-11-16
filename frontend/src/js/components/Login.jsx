import { useContext } from "react";
import { AuthContext } from "../contexts/AuthContext.jsx";
import { Button, Form, Input } from "antd";

function Login() {
  const { login } = useContext(AuthContext);

  function handleSubmit(values) {
    login(values.username, values.password);
  }

  return (
    <Form
      name="register"
      onFinish={handleSubmit}
      labelCol={{ span: 8 }}
      wrapperCol={{ span: 16 }}
      style={{ maxWidth: 600 }}
      scrollToFirstError={{focus: true}}
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
          Login
        </Button>
      </Form.Item>
    </Form>
  );
}

export default Login;
