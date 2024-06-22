import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { loadErrorMessage, pageNotFoundMessage } from "../../utils/errors.js";

class TournamentDetailView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div class="container-fluid main-game scroll-on">
    <div id="tournament-container" class="static"></div>
  </div>
  <div id="message" class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
  </div>
`;

let tournament = null;

const tournamentDetail = (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "message");
    return;
  }

  const tournamentContainer = document.getElementById("tournament-container");
  tournamentContainer.innerHTML = response;

  const cancelBtn = document.getElementById("cancel-btn");
  if (cancelBtn != null) cancelBtn.addEventListener("click", cancelTournament);
  const deleteBtn = document.getElementById("delete-btn");
  if (deleteBtn != null) deleteBtn.addEventListener("click", deleteTournament);
};

const cancelTournament = async (e) => {
  e.preventDefault();

  await gameService.cancelTournament(tournament).then(async (response) => {
    if (response.status !== undefined) {
      const tournamentContainer = document.getElementById(
        "tournament-container"
      );
      tournamentContainer.innerHTML = "";
      loadErrorMessage(response, "message");
      return;
    }
    await gameService.tournament(tournament).then(tournamentDetail);
    // TODO: toast sucesso?
  });
};

const deleteTournament = async (e) => {
  e.preventDefault();

  await gameService.deleteTournament(tournament).then((response) => {
    if (response.status !== undefined) {
      const tournamentContainer = document.getElementById(
        "tournament-container"
      );
      tournamentContainer.innerHTML = "";
      loadErrorMessage(response, "message");
      return;
    }
    window.location.replace("#my-tournaments");
    // TODO: toast sucesso?
    return;
  });
};

const start = async (user) => {
  tournament = new URLSearchParams(window.location.search).get("t");
  if (tournament === null) {
    pageNotFoundMessage("message");
    return;
  }

  await gameService.tournament(tournament).then(tournamentDetail);
};

export default new TournamentDetailView(html, start);
