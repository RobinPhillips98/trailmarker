// Third-party libraries
import { useState, useEffect, useContext } from "react";
import { Col, Divider, Row } from "antd";

// Personal helpers
import api from "../../../api";
import useErrorMessage from "../../../services/hooks/useErrorMessage";

// Contexts
import { AuthContext } from "../../../contexts/AuthContext";

// Components
import PartyInfoForm from "./subcomponents/PartyInfoForm";
import CurrentDifficultyDisplay from "./subcomponents/CurrentDifficultyDisplay";
import XPBudget from "./subcomponents/XPBudget";
import EncounterControls from "./subcomponents/EncounterControls";
import SimulationControls from "./subcomponents/SimulationControls";

/**
 * An overview with information and options for the current encounter
 *
 * @typedef {object} OverviewProps
 * @property {object} selectedEnemies The currently selected enemies in the
 *  encounter
 * @property {function} handleLoad The function to select this encounter's
 *  enemies
 * @property {function} clearEncounter The function to clear all enemies from
 *  the encounter
 * @property {React.RefObject[]} refs References used by the opening tour to
 * target components
 *
 * @param {OverviewProps} props
 * @returns {React.ReactElement}
 */
export default function Overview(props) {
  const { selectedEnemies, handleLoad, clearEncounter, refs } = props;

  // State Variables
  const [useSaved, setUseSaved] = useState(false);
  const [colorBlind, setColorBlind] = useState(false);
  const [charactersSaved, setCharactersSaved] = useState(false);
  const [characters, setCharacters] = useState([]);
  const [partySize, setPartySize] = useState(4);
  const [partyLevel, setPartyLevel] = useState(1);
  const [budget, setBudget] = useState({});
  const [xp, setXP] = useState(0);
  const [difficulty, setDifficulty] = useState("");

  // Other variables
  const { token } = useContext(AuthContext);
  const { errorMessage } = useErrorMessage();

  const difficultyColors = colorBlind
    ? {
        trivial: "#164c64",
        low: "#0e288e",
        moderate: "#881a58",
        severe: "#b32db5",
        extreme: "#a53606",
      }
    : {
        trivial: "blue",
        low: "green",
        moderate: "yellow",
        severe: "orange",
        extreme: "red",
      };

  // Event Handler Functions

  function handleChangeSaved() {
    setUseSaved(!useSaved);
  }

  function handleChangeColorBlind() {
    setColorBlind(!colorBlind);
  }

  function handlePartySize(value) {
    setPartySize(value);
  }

  function handlePartyLevel(value) {
    setPartyLevel(value);
  }

  useEffect(() => {
    /**
     * Fetches the current user's characters from the database and sets the
     * party size and level based on the number of characters retrieved and
     * their level
     */
    async function getPartyInfoFromServer() {
      try {
        const response = await api.get("/characters", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (response.data.characters.length > 0) {
          const fetchedCharacters = response.data.characters;

          setCharacters(fetchedCharacters);
          setCharactersSaved(true);
        } else {
          setCharactersSaved(false);
        }
      } catch (error) {
        errorMessage("Error fetching characters", error);
      }
    }
    if (token) getPartyInfoFromServer();
    else {
      setUseSaved(false);
      setCharactersSaved(false);
    }
  }, [token]);

  useEffect(() => {
    if (useSaved) {
      setPartyLevel(characters.at(0).level);
      setPartySize(characters.length);
    } else {
      setPartyLevel(1);
      setPartySize(4);
    }
  }, [characters, useSaved]);

  useEffect(() => {
    /**
     * Sets XP budget based on party size
     */
    function adjustXPBudget() {
      const characterAdjustment = partySize - 4;
      const newBudget =
        // Math breaks at party size of 1, but what if only one character saved?
        // At party size of 2, trivial and low are equal, blame Paizo's math
        partySize > 1
          ? {
              trivial: 40 + 10 * characterAdjustment,
              low: 60 + 20 * characterAdjustment,
              moderate: 80 + 20 * characterAdjustment,
              severe: 120 + 30 * characterAdjustment,
              extreme: 160 + 40 * characterAdjustment,
            }
          : {
              trivial: 5,
              low: 10,
              moderate: 20,
              severe: 30,
              extreme: 40,
            };
      setBudget(newBudget);
    }

    adjustXPBudget();
  }, [partySize]);

  useEffect(() => {
    /**
     * Set earned XP based on selected enemies and party level
     */
    function adjustXP() {
      let accumXP = 0;
      selectedEnemies.forEach((currentEnemy) => {
        const levelDifference = currentEnemy.level - partyLevel;
        if (levelDifference > 4) accumXP += 200 * currentEnemy.quantity;
        else if (levelDifference <= -4) accumXP += 5 * currentEnemy.quantity;
        else {
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
            default:
              console.error("Invalid enemy level entered");
              break;
          }
        }
      });
      setXP(accumXP);
    }

    adjustXP();
  }, [selectedEnemies, partyLevel]);

  useEffect(() => {
    /**
     * Set difficulty based on total XP with current XP budget
     */
    function adjustDifficulty() {
      if (xp < budget.low) setDifficulty("trivial");
      else if (xp >= budget.low && xp < budget.moderate) setDifficulty("low");
      else if (xp >= budget.moderate && xp < budget.severe)
        setDifficulty("moderate");
      else if (xp >= budget.severe && xp < budget.extreme)
        setDifficulty("severe");
      else setDifficulty("extreme");
    }

    adjustDifficulty();
  }, [xp, budget]);

  return (
    <div style={{ width: "100%" }}>
      <SimulationControls
        selectedEnemies={selectedEnemies}
        charactersSaved={charactersSaved}
        refs={refs}
      />

      <Row ref={refs[0]} gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} md={8}>
          <PartyInfoForm
            partySize={partySize}
            partyLevel={partyLevel}
            switched={useSaved}
            charactersSaved={charactersSaved}
            handlePartySize={handlePartySize}
            handlePartyLevel={handlePartyLevel}
            handleChange={handleChangeSaved}
            ref={refs[1]}
          />
        </Col>

        <Col xs={24} sm={12} md={8}>
          <XPBudget
            budget={budget}
            switched={colorBlind}
            handleChange={handleChangeColorBlind}
            colors={difficultyColors}
          />
        </Col>

        <Col xs={24} md={8}>
          <CurrentDifficultyDisplay
            difficulty={difficulty}
            xp={xp}
            colors={difficultyColors}
          />
        </Col>
      </Row>

      <Divider />

      <Row gutter={[16, 16]}>
        <Col span={24}>
          <EncounterControls
            enemies={selectedEnemies}
            clearEncounter={clearEncounter}
            handleLoad={handleLoad}
          />
        </Col>
      </Row>
    </div>
  );
}
