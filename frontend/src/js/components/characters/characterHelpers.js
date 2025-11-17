/**
 * A list with the available ancestry options, formatted to be the options of a
 * select component
 */
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

/**
 * A list with the available background options, formatted to be the options of a
 * select component
 */
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

/**
 * A list with the available class options, formatted to be the options of a
 * select component
 */
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

/**
 * A list of the attributes in Pathfinder
 */
export const attributes = [
  "strength",
  "dexterity",
  "constitution",
  "intelligence",
  "wisdom",
  "charisma",
];

/**
 * A list of the skills in Pathfinder
 */
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

/**
 * A list of the damage types in Pathfinder, formatted to be the options of a
 * select component
 */
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

/**
 * A list of the saving throws in Pathfinder
 */
export const saves = ["fortitude", "reflex", "will"];

/**
 * Convert a given string to title case
 *
 * @param {string} str The string to be converted
 * @returns {string}
 */
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

/**
 * Convert a given camel case string to a standard spaced string
 *
 * @param {string} str The string to be converted
 * @returns {string}
 */
export function splitCamelCase(str) {
  return str
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/([A-Z])([A-Z][a-z])/g, "$1 $2");
}
