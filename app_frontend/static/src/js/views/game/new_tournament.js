import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { setGameRulesLogic } from "./rules.js";

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

const loadErrorMessage = (error) => {
  const swapContainer = document.getElementById("add-tournament-container");
  swapContainer.innerHTML = /*html*/ `
    <h1 class="game-message text-center">${error.status} <br> ${error.message}</h1>`;
};

const putTournamentForm = (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response);
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

const start = async (user) => {
  gameService.getFormTournament().then(putTournamentForm);
};

export default new NewTournamentView(html, start);
