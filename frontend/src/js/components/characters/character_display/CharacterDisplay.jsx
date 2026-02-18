import CharacterHeader from "./subcomponents/CharacterHeader";
import CharacterBasics from "./subcomponents/CharacterBasics";
import CoreStats from "./subcomponents/CoreStats";
import AttributeModifiers from "./subcomponents/AttributeModifiers";
import SavesSection from "./subcomponents/SavesSection";
import SkillsSection from "./subcomponents/SkillsSection";
import AttacksSection from "./subcomponents/AttacksSection";
import SpellcastingSection from "./subcomponents/SpellcastingSection";
import CharacterControls from "./subcomponents/CharacterControls";
/**
 * A component to display information about a given character
 *
 * @param {object} props
 * @param {object} props.character The character being displayed
 * @param {function} props.deleteCharacter The function to delete the displayed character
 * @returns {JSX.element}
 */
export default function CharacterDisplay({ character, deleteCharacter }) {
  return (
    <div>
      <CharacterControls
        character={character}
        deleteCharacter={deleteCharacter}
      />
      <CharacterHeader character={character} />
      <CharacterBasics character={character} />
      <CoreStats character={character} />
      <AttributeModifiers character={character} />
      <SavesSection character={character} />
      <SkillsSection character={character} />
      <AttacksSection character={character} />
      <SpellcastingSection character={character} />
    </div>
  );
}
