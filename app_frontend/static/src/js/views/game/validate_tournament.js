import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { loadErrorMessage, pageNotFoundMessage } from "../../utils/errors.js";

class ValidateTournamentView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div class="main-game scroll-on container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
    <div id="verify-tournament-container" class="static"></div>
  </div>
`;

let tournament = null;

const putVerifyTable = async (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "verify-tournament-container");
    return;
  }

  const swapContainer = document.getElementById("verify-tournament-container");
  swapContainer.innerHTML = response;

  const verifyForms = document.querySelectorAll("form");
  verifyForms.forEach((form) => {
    form.addEventListener("submit", submitVerifyForm);
  });
};

const submitVerifyForm = async (e) => {
  e.preventDefault();
  const form = e.srcElement;
  const player = form.id.split("-").pop();
  const formData = new FormData(form);

  await gameService
    .validateTournament(tournament, player, formData)
    .then(verifyPlayerResult);
};

const verifyPlayerResult = async (response) => {
  if (typeof response === "string") {
    putVerifyTable(response);
  } else {
    if (response.hasOwnProperty("is_success") && response.is_success === true) {
      window.location.href = "?t=" + tournament + "#tournament";
      return;
    }
  }
  loadErrorMessage(response, "verify-tournament-container");
};

const start = async (user) => {
  tournament = new URLSearchParams(window.location.search).get("t");
  if (tournament === null) {
    pageNotFoundMessage("message");
    return;
  }

  await gameService.validateTournamentForm(tournament).then(putVerifyTable);
};

export default new ValidateTournamentView(html, start);
