import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { setGameRulesLogic } from "./rules.js";
import { loadErrorMessage } from "../../utils/errors.js";

class NewTournamentView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
    <div id="add-tournament-container"></div>
  </div>
`;

const putTournamentForm = (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "add-tournament-container");
    return;
  }

  const swapContainer = document.getElementById("add-tournament-container");
  swapContainer.innerHTML = response;

  const addTournamentForm = document.getElementById("tournament-form");
  addTournamentForm.addEventListener("submit", submitTournamentForm);

  setGameRulesLogic();
};

const submitTournamentForm = async (e) => {
  e.preventDefault();
  const addTournamentForm = document.getElementById("tournament-form");
  const formData = new FormData(addTournamentForm);

  await gameService.addTournament(formData).then(addGameResult);
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

  loadErrorMessage(response, "add-tournament-container");
};

const start = async (user) => {
  gameService.getFormTournament().then(putTournamentForm);
};

export default new NewTournamentView(html, start);
