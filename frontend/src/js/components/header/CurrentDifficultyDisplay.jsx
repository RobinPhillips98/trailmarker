function CurrentDifficultyDisplay(props) {
  return (
    <p>
      Current Difficulty: {props.difficulty} ({props.xp})
    </p>
  );
}

export default CurrentDifficultyDisplay;
