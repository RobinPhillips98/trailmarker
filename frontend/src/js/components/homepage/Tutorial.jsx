import { Button, Tour } from "antd";

/**
 * A component to display a tutorial to a new user.
 *
 * @typedef {object} TutorialProps
 * @property {boolean} open Whether or not the tour is open
 * @property {function} setOpen The function to set the value of `open`
 * @property {React.RefObject[]} refs The targets of the tour
 *
 * @param {TutorialProps} props
 * @returns
 */
export default function Tutorial(props) {
  const { open, setOpen, refs } = props;

  function handleClose() {
    localStorage.setItem("viewedTour", true);
    setOpen(false);
  }

  const skipButton = (
    <Button size="small" onClick={handleClose}>
      Skip Tutorial
    </Button>
  );

  const steps = [
    {
      title: "Welcome to Trailmarker! ",
      description:
        "With this tool you can build and run simulations of combat encounters for the Pathfinder Second Edition Beginner Box. Follow this tutorial to get started.",
    },
    {
      title: "Difficulty Calculator",
      description:
        "The difficulty calculator can be used to estimate the difficulty of an encounter before simulating it.",
      target: () => refs[0].current,
    },
    {
      title: "Difficulty Calculator Settings",
      description:
        "Here you can change the settings for the difficulty estimate, setting how many players and what party level it should use. Alternatively, after logging in, you can set it to use the characters you have saved.",
      target: () => refs[1].current,
    },
    {
      title: "Building Encounters",
      description:
        "To run the simulation, you must first build an encounter by selecting enemies.",
      target: () => refs[2].current,
    },
    {
      title: "Filtering Enemy List",
      description:
        'Here you can filter the enemy list to find just the type of enemy you\'re looking for. Try searching for the name "goblin" ',
      target: () => refs[3].current,
      placement: "down",
    },
    {
      title: "Selecting Enemies",
      description:
        'Here you can see information about each enemy and add an enemy to the encounter by pressing the "Add" button. Try adding some goblins to the encounter',
      target: () => refs[4].current,
    },
    {
      title: "Encounters",
      description:
        "Here you can view and edit the currently built encounter. With a user account, you can also use the controls above to save and load previously built encounters.",
      target: () => refs[5].current,
    },
    {
      title: "Simulation Options",
      description:
        "Here you can change the settings for the simulation itself. For now, you can only use pre-made characters, but with an account you can create your own custom characters.",
      target: () => refs[6].current,
    },
    {
      title: "Running the Simulation",
      description:
        "Finally, once you're ready, you can press this button to run the simulation!",
      target: () => refs[7].current,
    },
    {
      title: "How To",
      description:
        "If you'd like to read an overview of how to use Trailmarker, or if you want to view this tutorial again, you can do so here!",
      target: () => refs[8].current,
    },
  ];
  return (
    <Tour
      open={open}
      onClose={handleClose}
      steps={steps}
      actionsRender={(originNode, { current }) => (
        <>
          {current === 0 && skipButton}
          {originNode}
        </>
      )}
    />
  );
}
