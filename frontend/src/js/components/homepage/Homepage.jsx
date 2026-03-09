// Third-party libraries
import { useEffect, useRef, useState } from "react";
import { App, FloatButton, Typography } from "antd";

// Personal helpers
import api from "../../api";
import useErrorMessage from "../../services/hooks/useErrorMessage";

// Components
import Overview from "./overview/Overview";
import EncounterDisplay from "./encounter_display/EncounterDisplay";
import EnemyList from "./enemy_list/EnemyList";
import TutorialModal from "./overview/subcomponents/TutorialModal";
import Tutorial from "./Tutorial";

/**
 * The homepage of the site which displays information and options about the
 * current encounter, the enemies selected in the current encounter, and a list
 * of enemies that can be added to the current encounter. At the top of the
 * overview is a button to start the simulation.
 *
 * @returns {React.ReactElement}
 */
export default function Homepage() {
  const [tourOpen, setTourOpen] = useState(!localStorage.getItem("viewedTour"));

  const [selectedEnemies, setSelectedEnemies] = useState(
    JSON.parse(sessionStorage.getItem("enemies")) ?? [],
  );

  const { message } = App.useApp();
  const { Title } = Typography;
  const { errorMessage } = useErrorMessage;

  const refs = [];
  for (let i = 0; i <= 8; i++) {
    const ref = useRef(null);
    refs.push(ref);
  }

  useEffect(() => {
    sessionStorage.setItem("enemies", JSON.stringify(selectedEnemies));
  }, [selectedEnemies]);

  /**
   * Adds the given enemy to the encounter, or if it's already in the encounter,
   * increments its quantity
   *
   * @param {object} enemy The enemy to be added
   */
  function addEnemy(enemy) {
    const exists = selectedEnemies.some(
      (currentEnemy) => currentEnemy.id === enemy.id,
    );
    if (!exists) {
      enemy["quantity"] = 1;
      setSelectedEnemies((prev) => [...prev, enemy]);
    } else {
      incrementQuantity(enemy);
    }
  }

  /**
   * Increases the quantity of `enemy` by 1.
   *
   * Directly modifies enemy.quantity to ensure MAX_ENEMY_QUANTITY check in
   * Enemy.jsx works properly
   *
   * @param {object} enemy The enemy being altered
   */
  function incrementQuantity(enemy) {
    setSelectedEnemies((prev) => {
      prev.map((currentEnemy) => {
        if (currentEnemy.id === enemy.id) currentEnemy.quantity++;
      });
      return [...prev];
    });
  }

  /**
   * Decreases the quantity of `enemy` by 1
   *
   * Directly modifies enemy.quantity to ensure MAX_ENEMY_QUANTITY check in
   * Enemy.jsx works properly
   *
   * @param {object} enemy The enemy being altered
   */
  function decrementQuantity(enemy) {
    if (enemy.quantity === 1) removeEnemy(enemy);
    else {
      setSelectedEnemies((prev) => {
        prev.map((currentEnemy) => {
          if (currentEnemy.id === enemy.id) currentEnemy.quantity--;
        });
        return [...prev];
      });
    }
  }

  /**
   * Removes `enemy` from the encounter
   *
   * @param {object} enemy The enemy being altered
   */
  function removeEnemy(enemy) {
    enemy.quantity = 0;
    setSelectedEnemies((prev) =>
      prev.filter((currentEnemy) => currentEnemy !== enemy),
    );
  }

  /**
   * Removes all enemies from the encounter.
   */
  function clearEnemies() {
    selectedEnemies.forEach((enemy) => (enemy.quantity = 0));
    setSelectedEnemies([]);
    sessionStorage.removeItem("enemies");
  }

  /**
   * Overwrites the current encounter by clearing its enemies and adding the
   * enemies from the given encounter instead
   *
   * @param {object} encounter The encounter to be loaded
   */
  async function loadEncounter(encounter) {
    try {
      clearEnemies();
      const newEnemies = await Promise.all(
        encounter.enemies.map(async (enemy) => {
          const response = await api.get(`enemies/${enemy.id}`);
          const currentEnemy = response.data;
          currentEnemy.quantity = enemy.quantity;
          return currentEnemy;
        }),
      );
      setSelectedEnemies(newEnemies);
      message.success("Encounter loaded!");
    } catch (error) {
      errorMessage("Error loading encounter", error);
    }
  }

  return (
    <>
      <Tutorial refs={refs} open={tourOpen} setOpen={setTourOpen} />
      <Title style={{ marginLeft: 10 }}>Trailmarker</Title>
      <Overview
        selectedEnemies={selectedEnemies}
        clearEncounter={clearEnemies}
        handleLoad={loadEncounter}
        refs={refs}
      />
      <br />
      <EncounterDisplay
        handleRemove={removeEnemy}
        handleDecrement={decrementQuantity}
        handleAdd={incrementQuantity}
        enemies={selectedEnemies}
        ref={refs[5]}
      />
      <br />
      <EnemyList handleAdd={addEnemy} refs={refs} />
      <FloatButton.Group>
        <TutorialModal setTourOpen={setTourOpen} ref={refs[8]} />
        <FloatButton.BackTop />
      </FloatButton.Group>
    </>
  );
}
