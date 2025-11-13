import { useState } from "react";
import { ConfigProvider, theme } from "antd";

import EncounterDisplay from "./components/encounter_display/EncounterDisplay";
import EnemyList from "./components/enemy_list/EnemyList";
import api from "./api";
import Overview from "./components/overview/Overview";

function App() {
  const [selectedEnemies, setSelectedEnemies] = useState([]);

  function addEnemy(enemy) {
    const exists = selectedEnemies.some(
      (currentEnemy) => currentEnemy.id === enemy.id
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
      prev.filter((currentEnemy) => currentEnemy !== enemy)
    );
  }

  function clearEnemies() {
    setSelectedEnemies([]);
  }

  async function loadEncounter(encounter) {
  const newEnemies = await Promise.all(
    encounter.enemies.map(async (enemy) => {
      const response = await api.get(`enemies/${enemy.id}`);
      const currentEnemy = response.data;
      currentEnemy.quantity = enemy.quantity;
      return currentEnemy;
    })
  );

  setSelectedEnemies(newEnemies);
}


  const themeConfig = {
    token: {
      colorPrimary: "#722ed1",
      colorInfo: "#722ed1",
    },
    algorithm: theme.darkAlgorithm,
  };

  return (
    <ConfigProvider theme={themeConfig}>
      <main>
        <Overview
          selectedEnemies={selectedEnemies}
          clearEncounter={clearEnemies}
          handleLoad={loadEncounter}
        />
        <EncounterDisplay
          handleRemove={removeEnemy}
          handleDecrement={decrementQuantity}
          handleAdd={incrementQuantity}
          clearEncounter={clearEnemies}
          enemies={selectedEnemies}
        />
        <EnemyList handleAdd={addEnemy} />
      </main>
    </ConfigProvider>
  );
}

export default App;
