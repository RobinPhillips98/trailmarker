import PartyInfoForm from "./PartyInfoForm";
import CurrentDifficultyDisplay from "./CurrentDifficultyDisplay";
import XPBudget from "./XPBudget";
import NavBar from "./NavBar";

function Header(props) {
  return (
    <header>
      <PartyInfoForm
        handlePartySize={props.handlePartySize}
        handlePartyLevel={props.handlePartyLevel}
      />
      <CurrentDifficultyDisplay difficulty={props.difficulty} xp={props.xp} />
      <XPBudget budget={props.budget} />
      {/* <NavBar /> */}
    </header>
  );
}

export default Header;
