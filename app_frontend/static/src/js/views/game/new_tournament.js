import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { setGameRulesDynamicBehavior } from "./rules.js";
import { setTournamentFormDynamicBehavior } from "./tournament_dynamic.js";
import { loadErrorMessage } from "../../utils/errors.js";
import { CustomEvents } from "../../constants/custom-events.js";

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

  setGameRulesDynamicBehavior();
  setTournamentFormDynamicBehavior();
};

const submitTournamentForm = async (e) => {
  e.preventDefault();
  const addTournamentForm = document.getElementById("tournament-form");
  const formData = new FormData(addTournamentForm);

  await gameService.addTournament(formData).then(addTournamentResult);
};

const addTournamentResult = async (response) => {
  if (typeof response === "string") {
    putTournamentForm(response);
  } else {
    if (response.hasOwnProperty("is_success") && response.is_success === true) {
      if (
        response.hasOwnProperty("data") &&
        response.data.hasOwnProperty("tournament") &&
        response.data.hasOwnProperty("invite") &&
        response.data.tournament !== null &&
        response.data.invite != null
      ) {
        try {
          authService.sendGame2Factor(response.data.invite);
        } catch (error) {}
        window.location.href =
          "?t=" + response.data.tournament + "#verify-players";
        return;
      }
    }
  }

  loadErrorMessage(response, "add-tournament-container");
};

const start = async (user) => {
  await gameService.getFormTournament().then(putTournamentForm);

  window.addEventListener(CustomEvents.LANGUAGE_CHANGE_EVENT, async (e) => {
    await gameService.getFormTournament().then(putTournamentForm);
  });
};

export default new NewTournamentView(html, start);
