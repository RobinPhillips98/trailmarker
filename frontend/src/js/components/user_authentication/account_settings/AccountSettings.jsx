import { Tabs, Typography } from "antd";

import EditUsername from "./subcomponents/EditUsername";
import EditPassword from "./subcomponents/EditPassword";
import DeleteAccount from "./subcomponents/DeleteAccount";

export default function AccountSettings() {
  const { Title } = Typography;

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
