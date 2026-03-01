/**
 * Convert a given string to title case, splitting on whitespace, `-` and `_`
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
    .split(/[\s-_]/)
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

/**
 * Checks if a given object is empty, returns true if so, false if not.
 *
 * @param {object} obj The object being checked
 * @returns {boolean}
 */
export function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}

/**
 * Logs the error to the console and displays an alert to the user.
 *
 * @param {string} message Message to be displayed summarizing the error.
 * @param {object} error The full error object
 */
export function errorAlert(message, error) {
  console.error(message, error);
  alert(`${message}: ${error.response.data.detail}`);
}

/**
 * Returns `n` unique random elements from `arr`
 *
 * Source - https://stackoverflow.com/a/19270021
 *
 * Posted by Bergi, modified by community. See post 'Timeline' for change history
 *
 * Retrieved 2026-02-17, License - CC BY-SA 4.0
 *
 * @param {Array} arr The array to be sampled from
 * @param {number} n The number of elements to sample
 * @returns {Array}
 */
export function getRandom(arr, n) {
  var result = new Array(n),
    len = arr.length,
    taken = new Array(len);
  if (n > len)
    throw new RangeError("getRandom: more elements taken than available");
  while (n--) {
    var x = Math.floor(Math.random() * len);
    result[n] = arr[x in taken ? taken[x] : x];
    taken[x] = --len in taken ? taken[len] : len;
  }
  return result;
}

/**
 * Maximum quantity of an individual enemy
 */
export const MAX_ENEMY_QUANTITY = 25;

/**
 * A list of the available levels in the Pathfinder 2E beginner box, formatted
 * to be used as the options of a select component.
 */
export const levelOptions = [
  {
    value: 1,
    label: "1",
  },
  {
    value: 2,
    label: "2",
  },
  {
    value: 3,
    label: "3",
  },
];
