import SelectedEnemy from "./SelectedEnemy";

function EncounterDisplay(props) {
    return (
        <div id="encounterDisplay">
            <h2>Encounter</h2>
            <ul>
                {props.enemies.map((enemy) => (
                <li key={enemy.id}>
                    <SelectedEnemy
                        enemy={enemy}
                        handleRemove={props.handleRemove}
                        handleDecrement={props.handleDecrement}
                        handleAdd={props.handleAdd}/>
                </li>
                ))}
            </ul>
            
        </div>
    )

}

export default EncounterDisplay;