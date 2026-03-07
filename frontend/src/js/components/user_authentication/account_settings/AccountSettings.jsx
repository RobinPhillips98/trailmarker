// Third-party libraries
import { useContext } from "react";
import { Tabs, Typography } from "antd";

// Contexts
import { AuthContext } from "../../../contexts/AuthContext";

// Components
import EditUsername from "./subcomponents/EditUsername";
import EditPassword from "./subcomponents/EditPassword";
import DeleteAccount from "./subcomponents/DeleteAccount";
import NotAuthorized from "../../status_pages/NotAuthorized.jsx";

/**
 * A component to display account settings to the user.
 *
 * @returns {React.ReactElement}
 */
export default function AccountSettings() {
  const { token } = useContext(AuthContext);
  const { Title } = Typography;

  if (!token) return <NotAuthorized />;

  const items = [
    {
      key: 0,
      label: "Change Username",
      children: <EditUsername />,
    },
    {
      key: 1,
      label: "Change Password",
      children: <EditPassword />,
    },
    {
      key: 2,
      label: "Delete Account",
      children: <DeleteAccount />,
    },
  ];

  return (
    <>
      <Title>Account Settings</Title>
      <Tabs items={items} type="card" size="large" defaultActiveKey="1" />
    </>
  );
}
