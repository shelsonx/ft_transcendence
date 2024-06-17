export const getTimeValue = (value) => {
  if (!value) return "00";
  if (value < 10) return `0${value}`;
  return `${value}`;
};

export const timeDeltaToDuration = (delta) => {
  const minutes = Math.floor((delta % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((delta % (1000 * 60)) / 1000);

  return {
    minutes: minutes,
    seconds: seconds,
  };
};

export const durationToTimeDelta = (duration) => {
  return (duration.seconds + duration.minutes * 60) * 1000;
};
