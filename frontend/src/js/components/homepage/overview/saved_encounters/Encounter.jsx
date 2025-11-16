import { Button, Table } from "antd";

export default function Encounter({ handleLoad, handleDelete, encounter }) {
  function handleClickLoad() {
    handleLoad(encounter);
  }

  function handleClickDelete() {
    handleDelete(encounter);
  }

  const dataSource = encounter.enemies.map((enemy) => {
    return { ...enemy, ["key"]: enemy.id };
  });

  const columns = [
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
    },
    {
      title: "Quantity",
      dataIndex: "quantity",
      key: "quantity",
    },
  ];

  return (
    <div>
      <Table
        dataSource={dataSource}
        columns={columns}
        pagination={false}
        bordered={true}
        style={{ marginBottom: 10 }}
      />
      <Button
        type="primary"
        style={{ marginRight: 10 }}
        onClick={handleClickLoad}
      >
        Load Encounter
      </Button>
      <Button danger onClick={handleClickDelete}>
        Delete Encounter
      </Button>
    </div>
  );
}
