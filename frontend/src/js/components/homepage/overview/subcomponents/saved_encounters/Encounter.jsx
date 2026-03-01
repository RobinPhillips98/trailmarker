import { Button, Table } from "antd";
import { DeleteOutlined, DownloadOutlined } from "@ant-design/icons";

/**
 * A component for displaying information about a saved encounter
 *
 * @typedef {object} EncounterProps
 * @property {function} handleLoad The function to overwrite the current
 *  encounter with this encounter
 * @property {function} handleDelete The function to delete this encounter
 * @property {object} encounter The encounter to be displayed
 *
 * @param {EncounterProps} props
 * @returns {React.ReactElement}
 */
export default function Encounter(props) {
  const { handleLoad, handleDelete, encounter } = props;

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

  function handleClickLoad() {
    handleLoad(encounter);
  }

  function handleClickDelete() {
    handleDelete(encounter);
  }

  return (
    <>
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
        icon={<DownloadOutlined />}
      >
        Load Encounter
      </Button>
      <Button
        type="primary"
        danger
        onClick={handleClickDelete}
        icon={<DeleteOutlined />}
      >
        Delete Encounter
      </Button>
    </>
  );
}
