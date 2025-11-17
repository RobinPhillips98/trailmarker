import { useContext, useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Menu } from "antd";

import { AuthContext } from "../contexts/AuthContext";

/**
 * The nav bar at the top of the site, displaying links to the homepage and,
 * depending on whether the user is logged in, the pages to register and login, or
 * the page for saved characters and a button to log out.
 * 
 * @returns {JSX.Element}
 */
export default function NavBar() {
  const location = useLocation();
  const [current, setCurrent] = useState(location.pathname);

  const { user, token, logout } = useContext(AuthContext);

  useEffect(() => {
    setCurrent(location.pathname);
  }, [location]);

  const menuItems = (user && token)
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
