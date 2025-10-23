import { useState } from "react";

import Header from "./components/header/Header";
import EncounterDisplay from "./components/encounter_display/EncounterDisplay";
import EnemyList from "./components/enemy_list/EnemyList";


function App() {
    const [selectedEnemies, setSelectedEnemies] = useState([]);

    const addEnemy = (enemy) => {
        const exists = selectedEnemies.some((e) => {
            return e.id === enemy.id;
        })
        if (!exists) {
            enemy["quantity"] = 1;
            setSelectedEnemies(prev => [...prev, enemy]);
        } else {
            setSelectedEnemies((prev) => {
                prev.map((e) => {
                    if (e.id === enemy.id)
                        e.quantity++;
                });
                return [...prev];
            });
        }
    }

    const decrementQuantity = (enemy) => {
        if (enemy.quantity === 1) {
            removeEnemy(enemy);
            return;
        }
        const exists = selectedEnemies.some((e) => {
            return e.id === enemy.id;
        })
        if (!exists)
            return;
        else {
            setSelectedEnemies((prev) => {
                prev.map((e) => {
                    if (e.id === enemy.id) 
                        e.quantity--;
                });
                return [...prev];
            });
        }

    }

    const removeEnemy = (enemy) => {
        setSelectedEnemies((prev) => prev.filter(e => e !== enemy));
    }

    return (
        <>
            <Header/>
            <main>
                <EncounterDisplay
                    enemies={selectedEnemies}
                    handleRemove={removeEnemy}
                    handleDecrement={decrementQuantity}
                    handleAdd={addEnemy}
                />
                <EnemyList handleAdd={addEnemy}/>
            </main>
        </>
    );
}

export default App;