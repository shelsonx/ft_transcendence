export const getTimeValue = (value) => {
  if (!value) return "00";
  if (value < 10) return `0${value}`;
  return `${value}`;
};

export const timeDeltaToDuration = (delta) => {
  let seconds = delta / 1000;
  const minutes = Math.floor((seconds / 60));
  seconds = Math.floor((seconds % 60));

  return {
    minutes: minutes,
    seconds: seconds,
  };
};

export const durationToTimeDelta = (duration) => {
  if (duration === null) return null;
  return (duration.seconds + duration.minutes * 60) * 1000;
};
