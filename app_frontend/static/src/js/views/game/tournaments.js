import BaseLoggedView from '../baseLoggedView.js';
import gameService from '../../services/gameService.js';


class TournamentsView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start
    },
  );
  }
}

const html = /*html*/`
  <div class="d-flex justify-content-between">
    <h3 id="tournament-title">Tournaments</h3>
    <div >
      <button id="btn-data-switch" type="button" class="btn btn-info"
        onclick="window.location='#my-tournaments';"
      >
        My tournaments
      </button>
      <button id="btn-play" type="button" class="btn btn-primary"
        onclick="window.location='#add-tournament';"
      >
        Create tournament
      </button>
    </div>
  </div>
  <div class="container-fluid main-game scroll-on mt-3">
    <div id="tournament-table-container" class="static-list"></div>
  </div>
`

const swap = (response) => {
  // TODO: lidar quando retornar erro ou não responder
  const swapContainer = document.getElementById("tournament-table-container");
  swapContainer.innerHTML = response;
}

const start = async (user) => {
  await gameService.allTournaments().then(swap);
}

export default new TournamentsView(html, start);
