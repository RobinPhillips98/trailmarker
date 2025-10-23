import { useEffect, useState } from "react";

function CurrentDifficultyDisplay({ difficulty, xp }) {
  const [description, setDescription] = useState("");

  useEffect(() => {
    switch (difficulty) {
      case "trivial":
        setDescription(
          "Trivial-threat encounters are so easy that the characters have almost no chance of losing and rarely spend significant resources unless wasteful; they work best as warm-ups, palate cleansers, or reminders of the characters’ power."
        );
        break;
      case "low":
        setDescription(
          "Low-threat encounters offer a surface-level challenge that may use some of the party’s resources but rarely endanger the entire group unless they use very poor tactics."
        );
        break;
      case "moderate":
        setDescription(
          "Moderate-threat encounters pose a serious challenge that requires sound tactics and resource management, though the characters are still unlikely to be completely overpowered."
        );
        break;
      case "severe":
        setDescription(
          "Severe-threat encounters are among the toughest battles a group can win, suited for major story moments like boss fights, where poor tactics or bad luck could easily lead to death or retreat."
        );
        break;
      case "extreme":
        setDescription(
          "Extreme-threat encounters are nearly even matches for the characters and should be used sparingly—typically for climactic finales or highly skilled groups—since they carry a real risk of a total party defeat."
        );
        break;
      default:
        setDescription("Error: Invalid difficulty level");
    }
  }, [difficulty]);

  return (
    <div id="difficultyDisplay">
      <h2>
        Current Difficulty: {difficulty} ({xp})
      </h2>
      <p>{description}</p>
    </div>
  );
}

export default CurrentDifficultyDisplay;
