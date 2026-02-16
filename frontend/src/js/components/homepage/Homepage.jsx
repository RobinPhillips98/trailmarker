import { useState } from "react";

import api from "../../api";

import Overview from "./overview/Overview";
import EncounterDisplay from "./encounter_display/EncounterDisplay";
import EnemyList from "./enemy_list/EnemyList";
import { Typography } from "antd";

/**
 * The homepage of the site which displays information and options about the
 * current encounter, the enemies selected in the current encounter, and a list
 * of enemies that can be added to the current encounter.
 *
 * @returns {JSX.Element}
 */
export default function Homepage() {
  const [selectedEnemies, setSelectedEnemies] = useState([]);
  const { Title } = Typography;

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

  function incrementQuantity(enemy) {
    setSelectedEnemies((prev) => {
      prev.map((currentEnemy) => {
        if (currentEnemy.id === enemy.id) currentEnemy.quantity++;
      });
      return [...prev];
    });
  }

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

  function removeEnemy(enemy) {
    setSelectedEnemies((prev) =>
      prev.filter((currentEnemy) => currentEnemy !== enemy),
    );
  }

  function clearEnemies() {
    setSelectedEnemies([]);
  }

  /**
   * Overwrites the current encounter by clearing its enemies and adding the
   * enemies from the given encounter instead
   *
   * @param {object} encounter The encounter to be loaded
   */
  async function loadEncounter(encounter) {
    const newEnemies = await Promise.all(
      encounter.enemies.map(async (enemy) => {
        const response = await api.get(`enemies/${enemy.id}`);
        const currentEnemy = response.data;
        currentEnemy.quantity = enemy.quantity;
        return currentEnemy;
      }),
    );

    setSelectedEnemies(newEnemies);
  }

  return (
    <>
      <Title>Trailmarker</Title>
      <Overview
        selectedEnemies={selectedEnemies}
        clearEncounter={clearEnemies}
        handleLoad={loadEncounter}
      />
      <br />
      <EncounterDisplay
        handleRemove={removeEnemy}
        handleDecrement={decrementQuantity}
        handleAdd={incrementQuantity}
        enemies={selectedEnemies}
      />
      <br />
      <EnemyList handleAdd={addEnemy} />
    </>
  );
}
