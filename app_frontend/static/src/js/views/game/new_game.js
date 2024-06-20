import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { setGameRulesLogic } from "./rules.js";
import { loadErrorMessage } from "../../utils/errors.js";

class NewGameView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
    <div id="add-game-container"></div>
  </div>
`;

const putGameForm = async (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "add-game-container");
    return;
  }

  const swapContainer = document.getElementById("add-game-container");
  swapContainer.innerHTML = response;

  const addGameForm = document.getElementById("match-form");
  addGameForm.addEventListener("submit", submitGameForm);

  setGameRulesLogic();
};

const submitGameForm = async (e) => {
  e.preventDefault();
  const addGameForm = document.getElementById("match-form");
  const formData = new FormData(addGameForm);

  await gameService.addGame(formData).then(addGameResult);
};

const addGameResult = async (response) => {
  if (typeof response === "string") {
    putGameForm(response);
  } else {
    if (response.hasOwnProperty("is_success") && response.is_success === true) {
      if (
        response.hasOwnProperty("data") &&
        response.data.hasOwnProperty("game") &&
        response.data.game !== null
      ) {
        window.location.href =
          "?match=" + response.data.game + "#verify-player";
        return;
      }
    }
  }

  loadErrorMessage(response, "add-game-container");
};

const start = async (user) => {
  await gameService.getFormGame().then(putGameForm);
};

export default new NewGameView(html, start);
