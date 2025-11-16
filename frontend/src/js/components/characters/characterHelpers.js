export const ancestries = [
  {
    value: "dwarf",
    label: "Dwarf",
  },
  {
    value: "elf",
    label: "Elf",
  },
  {
    value: "human",
    label: "Human",
  },
];

export const backgrounds = [
  {
    value: "acolyte",
    label: "Acolyte",
  },
  {
    value: "criminal",
    label: "Criminal",
  },
  {
    value: "deckhand",
    label: "Deckhand",
  },
  {
    value: "farmhand",
    label: "Farmhand",
  },
  {
    value: "gambler",
    label: "Gambler",
  },
  {
    value: "scholar",
    label: "Scholar",
  },
  {
    value: "warrior",
    label: "Warrior",
  },
];

export const classes = [
  {
    value: "cleric",
    label: "Cleric",
  },
  {
    value: "fighter",
    label: "Fighter",
  },
  {
    value: "rogue",
    label: "Rogue",
  },
  {
    value: "wizard",
    label: "Wizard",
  },
];

export const attributes = [
  "strength",
  "dexterity",
  "constitution",
  "intelligence",
  "wisdom",
  "charisma",
];

export const skills = [
  "acrobatics",
  "arcana",
  "athletics",
  "crafting",
  "deception",
  "diplomacy",
  "intimidation",
  "lore",
  "medicine",
  "nature",
  "occultism",
  "performance",
  "religion",
  "society",
  "stealth",
  "survival",
  "thievery",
];

export const damageTypes = [
  {
    value: "bludgeoning",
    label: "Bludgeoning",
  },
  {
    value: "piercing",
    label: "Piercing",
  },
  {
    value: "slashing",
    label: "Slashing",
  },
];

export const saves = ["fortitude", "reflex", "will"];

export function toTitleCase(str) {
  if (!str) {
    return "";
  }

  return str
    .toLowerCase()
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

export function splitCamelCase(camelCaseString) {
  return camelCaseString
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/([A-Z])([A-Z][a-z])/g, "$1 $2");
}
