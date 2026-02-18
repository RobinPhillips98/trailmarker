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

/**
 * Checks if a given object is empty, returns true if so, false if not.
 *
 * @param {object} obj The object being checked
 * @returns {boolean}
 */
export function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}

export function errorAlert(error, message) {
  console.error(message, error);
  alert(`${message}: ${error.response.statusText}`)
}

// Source - https://stackoverflow.com/a/19270021
// Posted by Bergi, modified by community. See post 'Timeline' for change history
// Retrieved 2026-02-17, License - CC BY-SA 4.0

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
