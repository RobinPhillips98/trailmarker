import { Button, Card } from "antd";

/**
 * A component to display an enemy that can be added to the encounter
 *
 * @param {object} props
 * @param {function} props.handleAdd The function to add the given enemy to the encounter
 * @param {object} props.enemy The enemy to be displayed
 * @returns {JSX.Element}
 */
export default function Enemy({ handleAdd, enemy }) {
  function handleClick() {
    handleAdd(enemy);
  }

  return (
    <Card
      size="small"
      title={enemy.name}
      style={{ marginTop: 10, height: 200, width: 300 }}
    >
      <p>Level: {enemy.level}</p>
      <p>
        Traits:{" "}
        {enemy.traits.map((trait, index, arr) => {
          if (index === arr.length - 1) return <span>{trait}</span>;
          else return <span>{trait} | </span>;
        })}
      </p>
      <Button type="primary" onClick={handleClick} className="addRemoveButton">
        Add
      </Button>
    </Card>
  );
}
