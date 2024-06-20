import { GameRuleType } from "../../contracts/game/gameRule.js";

export const setGameRulesLogic = () => {
  const setRulesButton = document.getElementById("set-rules-btn");
  setRulesButton.addEventListener("click", showRules);

  const useDefaultRulesButton = document.getElementById("default-rules-btn");
  useDefaultRulesButton.addEventListener("click", useDefaultRules);

  const closeRulesButton = document.getElementById("close-rules-btn");
  closeRulesButton.addEventListener("click", hideRules);

  updateGameRulesFields();
  const ruleTypeField = document.getElementById("id_rule_type");
  ruleTypeField.addEventListener("change", updateGameRulesFields);
}

const showRules = () => {
  const setRulesButton = document.getElementById("set-rules-btn");
  setRulesButton.classList.add("d-none");

  const formGameRules = document.getElementById("form-game-rules");
  formGameRules.classList.remove("d-none");
};

const hideRules = (e) => {
  e.preventDefault();
  const setRulesButton = document.getElementById("set-rules-btn");
  setRulesButton.classList.remove("d-none");

  const formGameRules = document.getElementById("form-game-rules");
  formGameRules.classList.add("d-none");
};

const useDefaultRules = (e) => {
  e.preventDefault();
  const ruleTypeField = document.getElementById("id_rule_type");
  const pointsToWinFieldInput = document.getElementById("id_points_to_win");

  ruleTypeField.value = GameRuleType.PLAYER_POINTS;
  pointsToWinFieldInput.setAttribute("value", 11);
  pointsToWinFieldInput.value = 11;
  updateGameRulesFields();
};

const updateGameRulesFields = () => {
  const ruleTypeField = document.getElementById("id_rule_type");
  const pointsToWinField = document.getElementById("points_to_win");
  const pointsToWinFieldInput = document.getElementById("id_points_to_win");
  const gameTotalPointsField = document.getElementById("game_total_points");
  const gameTotalPointsFieldInput = document.getElementById(
    "id_game_total_points"
  );
  const maxDurationField = document.getElementById("max_duration");
  const maxDurationFieldInput = document.getElementById("id_max_duration");

  if (ruleTypeField.value === GameRuleType.PLAYER_POINTS) {
    pointsToWinField.classList.remove("d-none");
    gameTotalPointsField.classList.add("d-none");
    maxDurationField.classList.add("d-none");
    pointsToWinFieldInput.required = true;
    gameTotalPointsFieldInput.required = false;
    maxDurationFieldInput.required = false;
    gameTotalPointsFieldInput.setAttribute("value", "");
    maxDurationFieldInput.setAttribute("value", "");
  } else if (ruleTypeField.value === GameRuleType.GAME_TOTAL_POINTS) {
    pointsToWinField.classList.add("d-none");
    gameTotalPointsField.classList.remove("d-none");
    maxDurationField.classList.add("d-none");
    pointsToWinFieldInput.required = false;
    gameTotalPointsFieldInput.required = true;
    maxDurationFieldInput.required = false;
    pointsToWinFieldInput.setAttribute("value", "");
    maxDurationFieldInput.setAttribute("value", "");
  } else if (ruleTypeField.value === GameRuleType.GAME_DURATION) {
    pointsToWinField.classList.add("d-none");
    gameTotalPointsField.classList.add("d-none");
    maxDurationField.classList.remove("d-none");
    pointsToWinFieldInput.required = false;
    gameTotalPointsFieldInput.required = false;
    maxDurationFieldInput.required = true;
    pointsToWinFieldInput.setAttribute("value", "");
    gameTotalPointsFieldInput.setAttribute("value", "");
  }
};
