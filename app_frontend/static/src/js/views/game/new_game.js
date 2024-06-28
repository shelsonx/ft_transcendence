import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import authService from "../../services/authService.js";
import { setGameRulesDynamicBehavior } from "./rules.js";
import { loadErrorMessage } from "../../utils/errors.js";
import { CustomEvents } from "../../constants/custom-events.js";

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

const getGameForm = async () => {
  await gameService.getFormGame().then(putGameForm);
};

const putGameForm = async (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "add-game-container");
    return;
  }

  const swapContainer = document.getElementById("add-game-container");
  swapContainer.innerHTML = response;

  const addGameForm = document.getElementById("match-form");
  addGameForm.addEventListener("submit", submitGameForm);

  setGameRulesDynamicBehavior();
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
    return;
  } else {
    if (response.hasOwnProperty("is_success") && response.is_success === true) {
      if (
        response.hasOwnProperty("data") &&
        response.data.hasOwnProperty("game") &&
        response.data.hasOwnProperty("invite") &&
        response.data.game !== null &&
        response.data.invite != null
      ) {
        try {
          authService.sendGame2Factor(response.data.invite);
        } catch (error) {}
        window.location.href =
          "?match=" + response.data.game + "#verify-player";
        return;
      }
    }
  }

  loadErrorMessage(response, "add-game-container");
};

const newGameHashChangeHandler = async () => {
  window.removeEventListener(
    CustomEvents.LANGUAGE_CHANGE_EVENT,
    getGameForm
  );
  window.removeEventListener("hashchange", newGameHashChangeHandler);
};

const start = async (user) => {
  await getGameForm();

  window.addEventListener(CustomEvents.LANGUAGE_CHANGE_EVENT, getGameForm);
  window.addEventListener("hashchange", newGameHashChangeHandler);
};

export default new NewGameView(html, start);
