import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { GameRuleType } from "../../contracts/game/gameRule.js";
class NewGameView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div id="swap-container" class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
  </div>
`;

const swapGameForm = async (response_content) => {
  const swapContainer = document.getElementById("swap-container");
  swapContainer.innerHTML = response_content;

  const addGameForm = document.getElementById("match-form");
  addGameForm.addEventListener("submit", submitGameForm);

  const setRulesButton = document.getElementById("set-rules-btn");
  setRulesButton.addEventListener("click", showRules);

  updateGameRulesFields();
  const ruleTypeField = document.getElementById("id_rule_type");
  ruleTypeField.addEventListener("change", updateGameRulesFields);
};

const submitGameForm = async (e) => {
  e.preventDefault();
  const addGameForm = document.getElementById("match-form");
  const formData = new FormData(addGameForm);

  // await gameService.getFormGame().then(addGameResult);
  await gameService.addGame(formData).then(addGameResult);
};

const showRules = () => {
  const setRulesButton = document.getElementById("set-rules-btn");
  setRulesButton.classList.add("d-none");

  const formGameRules = document.getElementById("form-game-rules");
  formGameRules.classList.remove("d-none");
};

const updateGameRulesFields = () => {
  const ruleTypeField = document.getElementById("id_rule_type");
  const pointsToWinField = document.getElementById("points_to_win");
  const pointsToWinFieldInput = document.getElementById("id_points_to_win");
  const gameTotalPointsField = document.getElementById("game_total_points");
  const gameTotalPointsFieldInput = document.getElementById("id_game_total_points");
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

const addGameResult = async (response_content) => {
  console.log(response_content);
  if (typeof response_content == "string") {
    swapGameForm(response_content);
  } else {
    if (response_content.hasOwnProperty("status") && response_content.status !== "success") {
      console.log("error");
      return;
    }
    if (
      response_content.hasOwnProperty("data") &&
      response_content.data.hasOwnProperty("game") &&
      response_content.data.game !== null
    ) {
      // window.location.href = '?match=' + response.data.game + '#pong';
      // return;
    }

    const gameForm = document.getElementById("match-form");
    gameForm.classList.add("d-none");
    const gameRules = document.getElementById("game-rules");
    gameRules.classList.add("d-none");
    const rulesElement = document.getElementById("match-confirmation");
    rulesElement.classList.remove("d-none");

    // const confirmButton = document.getElementById("button-start");
    // confirmButton.addEventListener("click", (e) => {})
  }
};

// new URLSearchParams(obj).toString();

const start = async () => {
  await gameService.getFormGame().then(swapGameForm);
};

export default new NewGameView(html, start);
