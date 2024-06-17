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

const userLabel = "My tournaments"
const userDescription = "Your tournaments"
const allUsersLabel = "All tournaments"
const allUsersDescription = "Tournaments"
let userData = false

const html = /*html*/`
  <div class="d-flex justify-content-between">
    <h3 id="tournament-title"></h3>
    <div >
      <button id="btn-data-switch" type="button" class="btn btn-info">
        ${userLabel}
      </button>
      <button id="btn-play" type="button" class="btn btn-primary"
        onclick="window.location='#add-tournament';"
      >
        Create tournament
      </button>
    </div>
  </div>
  <div class="container-fluid main scroll-on mt-3">
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

  const title = document.getElementById("tournament-title");
  title.innerHTML = allUsersDescription;

  const btnDataSwitch = document.getElementById("btn-data-switch");
  btnDataSwitch.addEventListener("click", async () => {
    userData = !userData

    if (userData) {
      await gameService.userTournaments(user.id).then(swap);
      btnDataSwitch.innerHTML = allUsersLabel;
      title.innerHTML = userDescription;
    }
    else {
      await gameService.allTournaments().then(swap);
      btnDataSwitch.innerHTML = userLabel;
      title.innerHTML = allUsersDescription;
    }
  });
}

export default new TournamentsView(html, start);
