function Enemy({ handleAdd, enemy }) {
  const handleClick = () => {
    handleAdd(enemy);
  };

  return (
    <div>
      <ul className="enemy">
        <li>{enemy.name}</li>
        <li>Level: {enemy.level}</li>
        <li>Traits: </li>
        {enemy.traits.map((trait) => (
          <li>{trait}</li>
        ))}
        <li>
          <button onClick={handleClick}>Add</button>
        </li>
      </ul>
    </div>
  );
}

export default Enemy;
