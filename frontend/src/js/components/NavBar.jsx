import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Menu } from "antd";

function NavBar() {
  const location = useLocation();
  const [current, setCurrent] = useState(location.pathname);

  useEffect(() => {
    setCurrent(location.pathname);
  }, [location])

  const menuItems = [
    {
      key: "/",
      label: <Link to="/">Home</Link>,
    },
    {
      key: "/register",
      label: <Link to="/register">Register</Link>,
    },
    {
      key: "/login",
      label: <Link to="/login">Login</Link>,
    },
  ];

  return (
    <Menu
      selectedKeys={[current]}
      mode="horizontal"
      items={menuItems}
    />
  );
}

export default NavBar;
