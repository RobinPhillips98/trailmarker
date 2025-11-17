import { Button, Table } from "antd";

/**
 * A component for displaying information about a saved encounter
 *
 * @typedef {object} EncounterProps
 * @property {function} handleLoad The function to select this encounter's enemies
 * @property {function} handleDelete The function to delete this encounter
 * @property {object} encounter The encounter to be displayed
 *
 * @param {EncounterProps} props
 * @returns {JSX.Element}
 */
export default function Encounter(props) {
  const { handleLoad, handleDelete, encounter } = props;

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
