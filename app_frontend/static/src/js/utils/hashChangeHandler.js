export const hashChangeHandler = (e) => {
  const notApplicableHashes = [
    "#view-user-games",
    "#pong",
    "#verify-player",
    "#tournament",
    "#verify-players",
    "#two-factor-auth"
  ]
  const hash = window.location.hash;
  if (!notApplicableHashes.includes(hash))
    window.location.href = window.location.origin + window.location.hash;
};
