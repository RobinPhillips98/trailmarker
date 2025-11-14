import { useState } from "react";
import { Link } from "react-router-dom";
import { Menu } from "antd";

function NavBar() {
  const [current, setCurrent] = useState("home");
  function onClick(e) {
    setCurrent(e.key);
  }

  const menuItems = [
    {
      key: "home",
      label: <Link to="/">Home</Link>,
    },
    {
      key: "register",
      label: <Link to="/register">Register</Link>,
    },
    {
      key: "login",
      label: <Link to="/login">Login</Link>,
    },
  ];

  return (
    <Menu
      onClick={onClick}
      selectedKeys={[current]}
      mode="horizontal"
      items={menuItems}
    />
  );
}

export default NavBar;
