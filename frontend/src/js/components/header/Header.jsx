import { useState, useEffect } from "react";

import PartyInfoForm from "./PartyInfoForm";
import CurrentDifficultyDisplay from "./CurrentDifficultyDisplay";
import XPBudget from "./XPBudget";
import NavBar from "./NavBar";

function Header() {
    const [partySize, setPartySize] = useState(4);
    const [partyLevel, setPartyLevel] = useState(1);
    const [budget, setBudget] = useState({});

    // Sets XP budget based on party size
    useEffect(() => {
        const characterAdjustment = partySize - 4;
        const budget = {
            trivial: 40 + (10 * characterAdjustment),
            low: 60 + (20 * characterAdjustment),
            moderate: 80 + (20 * characterAdjustment),
            severe: 120 + (30 * characterAdjustment),
            extreme: 160 + (40 * characterAdjustment),
        }
        setBudget(budget);
    }, [partySize]);

    const handlePartySize = (event) => {
        setPartySize(event.target.value);
    }

    const handlePartyLevel = (event) => {
        setPartyLevel(event.target.value);
    }

    return (
        <header>
            <PartyInfoForm handlePartySize={handlePartySize} partyLevel={partyLevel} handlePartyLevel = {handlePartyLevel} />
            <CurrentDifficultyDisplay difficulty="WIP" xp="" />
            <XPBudget budget={budget} />
            <NavBar />
        </header> 
    )
}

export default Header;