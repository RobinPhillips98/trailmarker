import { useContext, useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Menu, Button } from "antd";
import { AuthContext } from "../contexts/AuthContext";

function NavBar() {
  const location = useLocation();
  const [current, setCurrent] = useState(location.pathname);

  const { user, logout } = useContext(AuthContext);

  useEffect(() => {
    setCurrent(location.pathname);
  }, [location]);

  const menuItems = user
    ? [
        {
          key: "/",
          label: <Link to="/">Home</Link>,
        },
        {
          key: "/characters",
          label: <Link to="/characters">Saved Characters</Link>,
        },
        {
          key: "/login",
          label: <Link onClick={logout} >Logout</Link>,
          danger: true
        },
      ]
    : [
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

  return <Menu selectedKeys={[current]} mode="horizontal" items={menuItems} />;
}

export default NavBar;
