import Encounter from "./Encounter";

function SavedEncounters({ encounters, handleLoad, handleDelete }) {
  return (
    <div id="savedEncounters">
      <h2>Saved Encounters</h2>
      {encounters.map((encounter) => (
        <li key={encounter.id} className="savedEncounter">
          <Encounter
            encounter={encounter}
            handleLoad={handleLoad}
            handleDelete={handleDelete}
          />
        </li>
      ))}
    </div>
  );
}

export default SavedEncounters;
