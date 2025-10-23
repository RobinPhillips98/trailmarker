function XPBudget({ budget }) {
    return (
        <div id="difficultyList">
            <p>XP Budget</p>
            <ul>
                <li>Trivial: {budget.trivial} XP</li>
                <li>Low: {budget.low} XP</li>
                <li>Moderate: {budget.moderate} XP</li>
                <li>Severe: {budget.severe} XP</li>
                <li>Extreme: {budget.extreme} XP</li>
            </ul>
        </div>
        
    )
}

export default XPBudget;