import { Button, Card } from "antd";

export default function Enemy({ handleAdd, enemy }) {
  function handleClick() {
    handleAdd(enemy);
  }

  return (
    <Card size="small" title={enemy.name} style={{ width: 300 }}>
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
