import { useEffect, useState } from "react";
import { Typography, Card, Tag } from "antd";

import { toTitleCase } from "../../../services/helpers";

/**
 * A component to display information about the current difficulty of the encounter
 *
 * @param {object} props
 * @param {string} props.difficulty The name of the current difficulty
 * @param {number} props.xp The experience point cost of the current encounter
 * @returns {JSX.Element}
 */
export default function CurrentDifficultyDisplay({ difficulty, xp }) {
  const { Title, Text } = Typography;

  const [description, setDescription] = useState("");
  const [difficultyColor, setDifficultyColor] = useState("");

  // Set difficulty description and color based on current difficulty
  useEffect(() => {
    switch (difficulty) {
      case "trivial":
        setDescription(
          "Trivial-threat encounters are so easy that the characters have almost no chance of losing and rarely spend significant resources unless wasteful; they work best as warm-ups, palate cleansers, or reminders of the characters' power."
        );
        setDifficultyColor("green");
        break;
      case "low":
        setDescription(
          "Low-threat encounters offer a surface-level challenge that may use some of the party's resources but rarely endanger the entire group unless they use very poor tactics."
        );
        setDifficultyColor("cyan");
        break;
      case "moderate":
        setDescription(
          "Moderate-threat encounters pose a serious challenge that requires sound tactics and resource management, though the characters are still unlikely to be completely overpowered."
        );
        setDifficultyColor("blue");
        break;
      case "severe":
        setDescription(
          "Severe-threat encounters are among the toughest battles a group can win, suited for major story moments like boss fights, where poor tactics or bad luck could easily lead to death or retreat."
        );
        setDifficultyColor("orange");
        break;
      case "extreme":
        setDescription(
          "Extreme-threat encounters are nearly even matches for the characters and should be used sparingly—typically for climactic finales or highly skilled groups—since they carry a real risk of a total party defeat."
        );
        setDifficultyColor("red");
        break;
      default:
        setDescription("Error: Invalid difficulty level");
        setDifficultyColor("default");
    }
  }, [difficulty]);

  return (
    <Card style={{ height: "100%" }}>
      <div style={{ marginBottom: 16 }}>
        <Title level={4} style={{ marginTop: 0, marginBottom: 8 }}>
          Current Difficulty
        </Title>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <Tag color={difficultyColor} style={{ fontSize: "14px", margin: 0 }}>
            {toTitleCase(difficulty)}
          </Tag>
          <Text style={{ fontSize: "16px" }}>({xp} XP)</Text>
        </div>
      </div>
      <Text>{description}</Text>
    </Card>
  );
}