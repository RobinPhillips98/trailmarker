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
  return Object.keys(obj).length === 0
}