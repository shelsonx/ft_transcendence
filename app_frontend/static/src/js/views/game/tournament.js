import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";

class TournamentDetailView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
<!-- <div id="tournament-container" class="container-fluid main">
  Oi
</div> -->
  <div class="container-fluid main scroll-on">
    <div id="tournament-container" class="static"></div>
  </div>
  <div id="message" class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
  </div>
`;

const swap = (response) => {
  const add_tournament = document.getElementById("tournament-container");
  add_tournament.innerHTML = response;
};

const start = async (user) => {
  const tournament = new URLSearchParams(window.location.search).get("t");
  if (tournament === null) {
    const message = document.getElementById("message");
    message.innerHTML = /*html*/ `
      <h1 class="game-message" data-i18n-key="page-not-found--title">
        Page not Found
      </h1>`;
    return;
  }

  await gameService.tournament(tournament).then(swap);
};

export default new TournamentDetailView(html, start);
