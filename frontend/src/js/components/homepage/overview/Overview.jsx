import PartyInfoForm from "./PartyInfoForm";
import CurrentDifficultyDisplay from "./CurrentDifficultyDisplay";
import XPBudget from "./XPBudget";
import EncounterOptions from "../encounter_display/EncounterOptions";
import SavedEncounters from "./saved_encounters/SavedEncounters";
import { useState, useEffect } from "react";

function Overview({ selectedEnemies, handleLoad, clearEncounter }) {
  const [partySize, setPartySize] = useState(4);

  function handlePartySize(value) {
    setPartySize(value);
  }

  const [partyLevel, setPartyLevel] = useState(1);

  function handlePartyLevel(value) {
    setPartyLevel(value);
  }

  const [budget, setBudget] = useState({});

  // Sets XP budget based on party size
  useEffect(() => {
    const characterAdjustment = partySize - 4;
    const newBudget = {
      trivial: 40 + 10 * characterAdjustment,
      low: 60 + 20 * characterAdjustment,
      moderate: 80 + 20 * characterAdjustment,
      severe: 120 + 30 * characterAdjustment,
      extreme: 160 + 40 * characterAdjustment,
    };
    setBudget(newBudget);
  }, [partySize]);

  const [xp, setXP] = useState(0);

  // Set earned XP based on selected enemies and party level
  useEffect(() => {
    let accumXP = 0;
    selectedEnemies.forEach((currentEnemy) => {
      const levelDifference = currentEnemy.level - partyLevel;
      switch (levelDifference) {
        case -4:
          accumXP += 10 * currentEnemy.quantity;
          break;
        case -3:
          accumXP += 15 * currentEnemy.quantity;
          break;
        case -2:
          accumXP += 20 * currentEnemy.quantity;
          break;
        case -1:
          accumXP += 30 * currentEnemy.quantity;
          break;
        case 0:
          accumXP += 40 * currentEnemy.quantity;
          break;
        case 1:
          accumXP += 60 * currentEnemy.quantity;
          break;
        case 2:
          accumXP += 80 * currentEnemy.quantity;
          break;
        case 3:
          accumXP += 120 * currentEnemy.quantity;
          break;
        case 4:
          accumXP += 160 * currentEnemy.quantity;
          break;
      }
    });
    setXP(accumXP);
  }, [selectedEnemies, partyLevel]);

  const [difficulty, setDifficulty] = useState("");

  // Set difficulty based on total XP with current XP budget
  useEffect(() => {
    if (xp < budget.low) setDifficulty("trivial");
    else if (xp >= budget.low && xp < budget.moderate) setDifficulty("low");
    else if (xp >= budget.moderate && xp < budget.severe)
      setDifficulty("moderate");
    else if (xp >= budget.severe && xp < budget.extreme)
      setDifficulty("severe");
    else setDifficulty("extreme");
  }, [xp, budget]);

  return (
    <div style={{ display: "flex", gap: 10, justifyContent: "space-around" }}>
      <div style={{ alignContent: "space-around" }}>
        <SavedEncounters handleLoad={handleLoad} />
        <EncounterOptions
          enemies={selectedEnemies}
          clearEncounter={clearEncounter}
        />
      </div>
      <PartyInfoForm
        handlePartySize={handlePartySize}
        handlePartyLevel={handlePartyLevel}
      />
      <XPBudget budget={budget} />
      <CurrentDifficultyDisplay difficulty={difficulty} xp={xp} />
    </div>
  );
}

export default Overview;
