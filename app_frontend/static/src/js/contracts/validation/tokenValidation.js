export const isValidToken = (token) => {
  if (typeof(token) !== String) return false;
  if (token.length !== 6) return false;
  if (!containsOnlyDigits(token)) return false;
  return true;
}

export const containsOnlyDigits = (str) => {
  return /^\d+$/.test(str);
}
