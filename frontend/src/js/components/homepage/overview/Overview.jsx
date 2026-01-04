import { useState, useEffect, useContext } from "react";

import { AuthContext } from "../../../contexts/AuthContext";
import api from "../../../api";
import EncounterOptions from "../encounter_display/EncounterOptions";

import SavedEncounters from "./saved_encounters/SavedEncounters";
import PartyInfoForm from "./PartyInfoForm";
import CurrentDifficultyDisplay from "./CurrentDifficultyDisplay";
import XPBudget from "./XPBudget";
import { useNavigate } from "react-router-dom";
import { Button } from "antd";
import { isEmpty } from "../../../services/helpers";

/**
 * An overview with information and options for the current encounter
 *
 * @typedef {object} OverviewProps
 * @property {object} selectedEnemies The currently selected enemies in the encounter
 * @property {function} handleLoad The function to select this encounter's enemies
 * @property {function} clearEncounter The function to clear all enemies from the encounter
 *
 * @param {OverviewProps} props
 * @returns {JSX.Element}
 */
export default function Overview(props) {
  const { selectedEnemies, handleLoad, clearEncounter } = props;
  const [switched, setSwitched] = useState(false);

  const { token, user } = useContext(AuthContext);

  useEffect(() => {
    /**
     * Fetches the current user's characters from the database and sets the party
     * size and level based on the number of characters retrieved and their level
     */
    async function getPartyInfoFromServer() {
      try {
        const response = await api.get("/characters", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (response.data.characters.length > 0) {
          const characters = response.data.characters;
          setPartyLevel(characters.at(0).level);
          if (characters.length >= 2) setPartySize(characters.length);
          else {
            alert(
              "Less than 2 characters saved, setting party size to minimum 2"
            );
            setPartySize(2);
          }
        } else {
          alert("No saved characters!");
          setSwitched(false);
        }
      } catch (error) {
        console.error("Error fetching characters", error);
      }
    }
    if (switched) getPartyInfoFromServer();
  }, [switched, token]);

  function handleChange() {
    setSwitched(!switched);
  }

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

  const navigate = useNavigate();

  function handleClick() {
    navigate("/simulation/", { state: { enemies: selectedEnemies } });
  }

  return (
    <div style={{ display: "flex", gap: 10, justifyContent: "space-around" }}>
      <div style={{ alignContent: "space-around" }}>
        <Button
          type="primary"
          style={{ marginBottom: 10 }}
          onClick={handleClick}
          disabled={!user || isEmpty(selectedEnemies)}
        >
          Run Simulation
        </Button>
        <SavedEncounters handleLoad={handleLoad} />
        <EncounterOptions
          enemies={selectedEnemies}
          clearEncounter={clearEncounter}
        />
      </div>
      <PartyInfoForm
        partySize={partySize}
        partyLevel={partyLevel}
        switched={switched}
        handlePartySize={handlePartySize}
        handlePartyLevel={handlePartyLevel}
        handleChange={handleChange}
      />
      <XPBudget budget={budget} />
      <CurrentDifficultyDisplay difficulty={difficulty} xp={xp} />
    </div>
  );
}
