export const isValidToken = (token) => {
  if (token.length !== 6) return false;
  if (!containsOnlyDigits(token)) return false;
  return true;
}

export const containsOnlyDigits = (str) => {
  return /^\d+$/.test(str);
}
