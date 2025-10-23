function SelectedEnemy(props) {
    const enemy = props.enemy;

    function handleClickDecrement() {
        props.handleDecrement(enemy);
    }

    function handleClickRemove() {
        props.handleRemove(enemy);
    }

    function handleClickAdd() {
        props.handleAdd(enemy);
    }

    return (
        <ul className="enemy">
            <li>{enemy.name}</li>
            <li><button onClick={handleClickDecrement}>-</button></li>
            <li>{enemy.quantity}</li>
            <li><button onClick={handleClickAdd}>+</button></li>
            <button onClick={handleClickRemove}>Remove</button>
        </ul>
    )
}

export default SelectedEnemy;