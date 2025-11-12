function Encounter({ handleLoad, handleDelete, encounter }) {
  function handleClickLoad() {
    handleLoad(encounter);
  };

  function handleClickDelete() {
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
