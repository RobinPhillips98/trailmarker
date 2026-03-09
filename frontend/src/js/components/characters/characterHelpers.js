import { toTitleCase } from "../../services/helpers";

/**
 * A list with the available ancestry options, formatted to be used as the
 * options of a select component
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
 * A list of the available area typed, formatted to be used as the options of
 * a select component
 */
export const areaTypes = [
  {
    value: "burst",
    label: "Burst",
  },
  {
    value: "cone",
    label: "Cone",
  },
  {
    value: "emanation",
    label: "Emanation",
  },
  {
    value: "line",
    label: "Line",
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
 * A list with the available background options, formatted to be used as the
 * options of a select component
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
 * A list with the available class options, formatted to be used as the options
 *  of a select component
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
 * A list of the available dwarf heritages, formatted to be used as the options
 *  of a select component.
 */
export const dwarfHeritages = [
  {
    value: "death_warden",
    label: "Death Warden Dwarf",
  },
  {
    value: "forge",
    label: "Forge Dwarf",
  },
  {
    value: "rock",
    label: "Rock Dwarf",
  },
];

/**
 * A list of the available elf heritages, formatted to be used as the options
 *  of a select component.
 */
export const elfHeritages = [
  {
    value: "cavern",
    label: "Cavern Elf",
  },
  {
    value: "whisper",
    label: "Whisper Elf",
  },
  {
    value: "woodland",
    label: "Woodland Elf",
  },
];

/**
 * A list of the available human heritages, formatted to be used as the options
 *  of a select component.
 */
export const humanHeritages = [
  {
    value: "battle_trained",
    label: "Battle Trained",
  },
  {
    value: "skilled",
    label: "Skilled",
  },
  {
    value: "warden",
    label: "Warden",
  },
];

export const otherFeatures = [
  {
    value: "thief",
    label: "Thief",
  },
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
 * A list of the saving throws in Pathfinder
 */
export const saves = ["fortitude", "reflex", "will"];

/**
 * A list of the saving throws in Pathfinder, formatted to be used as the
 * options of a select component.
 */
export const saveOptions = saves.map((save) => {
  return {
    value: save,
    label: toTitleCase(save),
  };
});

const cantripOptions = [
  { label: "Gouging Claw", value: "gouging_claw" },
  { label: "Telekinetic Projectile", value: "telekinetic_projectile" },
  { label: "Vitality Lash", value: "vitality_lash" },
];

const firstRankSpellOptions = [
  { label: "Breathe Fire", value: "breathe_fire" },
  { label: "Force Barrage", value: "force_barrage" },
  { label: "Force Bolt", value: "force_bolt" },
];

const secondRankSpellOptions = [
  { label: "Acid Grip", value: "acid_grip" },
  { label: "Floating Flame", value: "floating_flame" },
];

/**
 * A list of all spells, formatted into option groups by level for a Select
 * component.
 */
export const spellOptions = [
  {
    label: "Cantrips",
    title: "cantrips",
    options: cantripOptions,
  },
  {
    label: "1st-Rank Spells",
    title: "1st-rank-spells",
    options: firstRankSpellOptions,
  },
  {
    label: "2nd-Rank Spells",
    title: "2nd-rank-spells",
    options: secondRankSpellOptions,
  },
];

const simpleMeleeOptions = [
  {
    label: "Club",
    value: "club",
  },
  {
    label: "Dagger",
    value: "dagger",
  },
  {
    label: "Mace",
    value: "mace",
  },
  {
    label: "Spear",
    value: "spear",
  },
  {
    label: "Staff",
    value: "staff",
  },
];

const martialMeleeOptions = [
  {
    label: "Battle Axe",
    value: "battle_axe",
  },
  {
    label: "Greataxe",
    value: "greataxe",
  },
  {
    label: "Greatsword",
    value: "greatsword",
  },
  {
    label: "Hatchet",
    value: "hatchet",
  },
  {
    label: "Light Hammer",
    value: "light_hammer",
  },
  {
    label: "Longsword",
    value: "longsword",
  },
  {
    label: "Maul",
    value: "maul",
  },
  {
    label: "Rapier",
    value: "rapier",
  },
  {
    label: "Scimitar",
    value: "scimitar",
  },
  {
    label: "Shortsword",
    value: "shortsword",
  },
  {
    label: "Starknife",
    value: "starknife",
  },
  {
    label: "Trident",
    value: "trident",
  },
  {
    label: "Warhammer",
    value: "warhammer",
  },
];

const simpleRangedOptions = [
  {
    label: "Crossbow",
    value: "crossbow",
  },
  {
    label: "Hand Crossbow",
    value: "hand_crossbow",
  },
  {
    label: "Javelin",
    value: "javelin",
  },
];

const martialRangedOptions = [
  {
    label: "Longbow",
    value: "longbow",
  },
  {
    label: "Shortbow",
    value: "shortbow",
  },
];

/**
 * A list of all weapons in the Pathfinder 2E beginner box, formatted into
 * option groups for a Select component.
 */
export const weaponOptions = [
  {
    label: "Simple Melee",
    title: "simple-melee",
    options: simpleMeleeOptions,
  },
  {
    label: "Martial Melee",
    title: "martial-melee",
    options: martialMeleeOptions,
  },
  {
    label: "Simple Ranged",
    title: "simple-ranged",
    options: simpleRangedOptions,
  },
  {
    label: "Martial Ranged",
    title: "martial-ranged",
    options: martialRangedOptions,
  },
];

/**
 * A list of the weapon types in Pathfinder 2E, formatted to be the options of
 * a Select component.
 */
export const weaponTypeOptions = [
  {
    label: "Simple",
    value: "simple",
  },
  {
    label: "Martial",
    value: "martial",
  },
  {
    label: "Fists",
    value: "fists",
  },
];

/**
 * A regex pattern used to verify a string is a valid damage roll
 */
export const damagePattern = /^[1-9]\d?d(4|6|8|10|12)([+-]\d{1,2})?$/i;
