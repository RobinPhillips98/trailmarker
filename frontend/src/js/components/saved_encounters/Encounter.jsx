function Encounter({ handleLoad, handleDelete, encounter }) {
  const handleClickLoad = () => {
    handleLoad(encounter);
  };

  const handleClickDelete = () => {
    handleDelete(encounter);
  };

  return (
    <div className="encounter">
        <h3>{encounter.name}</h3>
        <ul>
          {encounter.enemies.map((enemy) => (
            <li>
              {enemy.quantity} {enemy.name}
            </li>
          ))}
        </ul>
        <button onClick={handleClickLoad}>Load Encounter</button>
        <button onClick={handleClickDelete}>Delete Encounter</button>
    </div>
  );
}

export default Encounter;
