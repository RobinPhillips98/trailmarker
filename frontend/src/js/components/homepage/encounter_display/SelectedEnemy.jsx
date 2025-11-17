import { Button } from "antd";

/**
 *
 * A component to display an enemy that has been selected in the current encounter
 *
 * @typedef {object} SelectedEnemyProps
 * @property {object} enemy The enemy to be displayed
 * @property {function} handleRemove The function called when remove is clicked
 * @property {function} handleDecrement The function called when the minus button is clicked
 * @property {function} handleAdd The function called when the plus button is clicked
 *
 * @param {SelectedEnemyProps} props
 * @returns {JSX.Element}
 */
export default function SelectedEnemy(props) {
  const { enemy, handleRemove, handleDecrement, handleAdd } = props;

  function handleClickDecrement() {
    handleDecrement(enemy);
  }

  function handleClickRemove() {
    handleRemove(enemy);
  }

  function handleClickAdd() {
    handleAdd(enemy);
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
