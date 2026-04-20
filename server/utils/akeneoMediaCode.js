const MAX_CODE_LEN = 500;

/**
 * Akeneo media file "code" is a path-like string (e.g. 4/6/9/e/hash_filename.png).
 * Rejects traversal and unexpected characters.
 * @param {string} code
 */
export function isValidAkeneoMediaCode(code) {
  if (typeof code !== 'string' || code.length === 0 || code.length > MAX_CODE_LEN) {
    return false;
  }
  if (code.includes('..') || code.startsWith('/') || code.includes('\\')) {
    return false;
  }
  return /^[\w/.-]+$/.test(code);
}
