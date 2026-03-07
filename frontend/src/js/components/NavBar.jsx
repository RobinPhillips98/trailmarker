import { useContext, useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Button, Drawer, Grid, Menu } from "antd";
import {
  CloseOutlined,
  FolderOpenOutlined,
  FolderOutlined,
  HomeFilled,
  HomeOutlined,
  LoginOutlined,
  LogoutOutlined,
  MenuOutlined,
  UserAddOutlined,
  UserOutlined,
  UserSwitchOutlined,
} from "@ant-design/icons";

import { AuthContext } from "../contexts/AuthContext";

/**
 * The nav bar at the top of the site, displaying links to the homepage and,
 * depending on whether the user is logged in, the pages to register and login,
 * or the page for saved characters and a button to log out.
 *
 * @returns {React.ReactElement}
 */
export default function NavBar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const location = useLocation();
  const [current, setCurrent] = useState(location.pathname);
  const screens = Grid.useBreakpoint();
  const { user, token, logout } = useContext(AuthContext);

  useEffect(() => {
    setCurrent(location.pathname);
  }, [location]);

  const menuItems =
    user && token
      ? [
          {
            key: "/",
            label: <Link to="/">Home</Link>,
            icon: current === "/" ? <HomeFilled /> : <HomeOutlined />,
          },
          {
            key: "/characters",
            label: <Link to="/characters">Saved Characters</Link>,
            icon:
              current === "/characters" ? (
                <FolderOpenOutlined />
              ) : (
                <FolderOutlined />
              ),
          },
          {
            key: "/user_settings",
            label: user.username,
            icon: <UserOutlined />,
            children: [
              {
                key: "settings",
                label: <Link to="/user_settings">Account Settings</Link>,
                icon: <UserSwitchOutlined />,
              },
              {
                key: "logout",
                label: <Link onClick={logout}>Logout</Link>,
                danger: true,
                icon: <LogoutOutlined />,
              },
            ],
          },
        ]
      : [
          {
            key: "/",
            label: <Link to="/">Home</Link>,
            icon: current === "/" ? <HomeFilled /> : <HomeOutlined />,
          },
          {
            key: "/register",
            label: <Link to="/register">Register</Link>,
            icon: <UserAddOutlined />,
          },
          {
            key: "/login",
            label: <Link to="/login">Login</Link>,
            icon: <LoginOutlined />,
          },
        ];

  const handleMenuItemClick = (e) => {
    if (user && e.target?.firstChild?.textContent == user.username) return;
    setMobileMenuOpen(false);
  };

  // Desktop view
  if (screens.md) {
    return (
      <Menu
        selectedKeys={[current]}
        mode="horizontal"
        items={menuItems}
        style={{ borderBottom: "none" }}
      />
    );
  }

  // Mobile view
  else {
    return (
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "12px 16px",
          height: "auto",
          lineHeight: "1",
        }}
      >
        <Link
          to="/"
          style={{ fontSize: "18px", fontWeight: "bold", lineHeight: "1" }}
        >
          Trailmarker
        </Link>
        <Button
          type="text"
          icon={<MenuOutlined style={{ fontSize: "20px" }} />}
          onClick={() => setMobileMenuOpen(true)}
          style={{ padding: "4px 0" }}
        />

        <Drawer
          title="Menu"
          placement="right"
          onClose={() => setMobileMenuOpen(false)}
          open={mobileMenuOpen}
          closeIcon={<CloseOutlined />}
        >
          <Menu
            selectedKeys={[current]}
            mode="inline"
            items={menuItems.slice(1).map((item) => ({
              ...item,
              label: <div onClick={handleMenuItemClick}>{item.label}</div>,
              children: item.children?.map((child) => ({
                ...child,
                label: (
                  <div onClick={() => setMobileMenuOpen(false)}>
                    {child.label}
                  </div>
                ),
              })),
            }))}
            style={{ border: "none" }}
          />
        </Drawer>
      </div>
    );
  }
}
