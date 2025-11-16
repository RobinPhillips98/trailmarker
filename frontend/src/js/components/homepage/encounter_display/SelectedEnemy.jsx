import { Button } from "antd";

export default function SelectedEnemy(props) {
  const enemy = props.enemy;

  function handleClickDecrement() {
    props.handleDecrement(enemy);
  }

  function handleClickRemove() {
    props.handleRemove(enemy);
  }

  function handleClickAdd() {
    props.handleAdd(enemy);
  }

  return (
    <ul className="selectedEnemy">
      <li>{enemy.name}</li>
      <li>
        <Button color="volcano" variant="solid" onClick={handleClickDecrement}>
          -
        </Button>
      </li>
      <li>{enemy.quantity}</li>
      <li>
        <Button type="primary" onClick={handleClickAdd}>
          +
        </Button>
      </li>
      <Button
        style={{ marginLeft: 10 }}
        danger
        variant="filled"
        onClick={handleClickRemove}
        className="addRemoveButton"
      >
        Remove
      </Button>
    </ul>
  );
}
