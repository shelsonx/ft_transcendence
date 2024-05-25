export const getTimeValue = (value) => {
  if (!value)
    return "00";
  if (value < 10)
    return `0${value}`;
  return `${value}`;
}
