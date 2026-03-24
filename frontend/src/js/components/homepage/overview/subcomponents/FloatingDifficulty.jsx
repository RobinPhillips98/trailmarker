import { useEffect, useState } from "react";
import { Tag, theme, Typography } from "antd";
import { toTitleCase } from "../../../../services/helpers";

/**
 * A floating difficulty display that appears after the user scrolls down.
 *
 * @param {object} props
 * @param {string} props.difficulty The current encounter difficulty
 * @param {object} props.difficultyColors A mapping of  difficulty strings to
 *  colors
 * @param {number} props.xp The current encounter XP total
 * @returns {React.ReactElement}
 */

export default function FloatingDifficulty(props) {
  const { difficulty, difficultyColors, xp } = props;
  const [visible, setVisible] = useState(false);
  const { token: themeToken } = theme.useToken();
  const { Text } = Typography;

  useEffect(() => {
    const THRESHOLD = 200;

    function onScroll() {
      setVisible(window.scrollY > THRESHOLD);
    }

    onScroll();

    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  if (visible && difficulty)
    return (
      <div
        style={{
          position: "fixed",
          top: 8,
          right: 10,
          zIndex: 1000,

          background: themeToken.colorBgElevated,
          border: `1px solid ${themeToken.colorBorder}`,
          borderRadius: 999,
          padding: "6px 10px",

          display: "flex",
          alignItems: "center",
          gap: 10,
          pointerEvents: "none",
        }}
      >
        <Tag color={difficultyColors[difficulty]}>
          {toTitleCase(difficulty)}
        </Tag>

        <Text>{xp} XP</Text>
      </div>
    );
  else return null;
}
