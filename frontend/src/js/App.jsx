import { useState, useEffect } from "react";

import Header from "./components/header/Header";
import EncounterDisplay from "./components/encounter_display/EncounterDisplay";
import EnemyList from "./components/enemy_list/EnemyList";


function App() {
    const [selectedEnemies, setSelectedEnemies] = useState([]);

    const addEnemy = (enemy) => {
        const exists = selectedEnemies.some((targetEnemy) => {
            return targetEnemy.id === enemy.id;
        })
        if (!exists) {
            enemy["quantity"] = 1;
            setSelectedEnemies(prev => [...prev, enemy]);
        } else {
            setSelectedEnemies((prev) => {
                prev.map((targetEnemy) => {
                    if (targetEnemy.id === enemy.id)
                        targetEnemy.quantity++;
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
        const exists = selectedEnemies.some((targetEnemy) => {
            return targetEnemy.id === enemy.id;
        })
        if (!exists)
            return;
        else {
            setSelectedEnemies((prev) => {
                prev.map((targetEnemy) => {
                    if (targetEnemy.id === enemy.id) 
                        targetEnemy.quantity--;
                });
                return [...prev];
            });
        }

    }

    const removeEnemy = (enemy) => {
        setSelectedEnemies((prev) => prev.filter(e => e !== enemy));
    }

    const [partySize, setPartySize] = useState(4);

    const handlePartySize = (event) => {
        setPartySize(event.target.value);
    }

    const [partyLevel, setPartyLevel] = useState(1);

    const handlePartyLevel = (event) => {
        setPartyLevel(event.target.value);
    }

    const [budget, setBudget] = useState({});

    // Sets XP budget based on party size
    useEffect(() => {
        const characterAdjustment = partySize - 4;
        const newBudget = {
            trivial: 40 + (10 * characterAdjustment),
            low: 60 + (20 * characterAdjustment),
            moderate: 80 + (20 * characterAdjustment),
            severe: 120 + (30 * characterAdjustment),
            extreme: 160 + (40 * characterAdjustment),
        }
        setBudget(newBudget);
    }, [partySize]);

    const [xp, setXP] = useState(0);

    // Set earned XP based on selected enemies
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
        })
        setXP(accumXP);
    }, [selectedEnemies, partyLevel]);

    const [difficulty, setDifficulty] = useState("");

    // Set difficulty based on total XP with current XP budget
    useEffect(() => {
        if (xp < budget.low)
            setDifficulty("trivial");
        else if (xp >= budget.low && xp < budget.moderate)
            setDifficulty("low");
        else if (xp >= budget.moderate && xp < budget.severe)
            setDifficulty("moderate");
        else if (xp >= budget.severe && xp < budget.extreme)
            setDifficulty("severe");
        else
            setDifficulty("extreme");
    }, [xp, budget]);

    return (
        <>
            <Header
                handlePartySize={handlePartySize}
                handlePartyLevel={handlePartyLevel}
                budget={budget}
                xp={xp}
                difficulty={difficulty}
            />
            <main>
                <EncounterDisplay
                    handleRemove={removeEnemy}
                    handleDecrement={decrementQuantity}
                    handleAdd={addEnemy}
                    enemies={selectedEnemies}
                />
                <EnemyList handleAdd={addEnemy}/>
            </main>
        </>
    );
}

export default App;