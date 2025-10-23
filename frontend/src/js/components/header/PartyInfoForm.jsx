function PartyInfoForm(props) {
    return (
        <form>
            <p>Number of Players</p>
            <select name="partySize" id="partySize" onChange={props.handlePartySize}>
                <option value="2">2 Players</option>
                <option value="3">3 Players</option>
                <option value="4" selected>4 Players</option>
                <option value="5">5 Players</option>
                <option value="6">6 Players</option>
            </select>
            <p>Party Level</p>
            <select name="partyLevel" id="partyLevel" onChange={props.handlePartyLevel}>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
            </select>
        </form>
    );
}

export default PartyInfoForm;