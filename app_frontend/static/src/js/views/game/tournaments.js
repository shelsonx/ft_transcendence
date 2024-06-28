import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { CustomEvents } from "../../constants/custom-events.js";

class TournamentsView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div class="d-flex justify-content-between">
    <h3 id="tournament-title" data-i18n-key="tournaments-title">
      Tournaments
    </h3>
    <div >
      <button id="btn-data-switch" type="button" class="btn btn-info"
        onclick="window.location='#my-tournaments';" data-i18n-key="my-tournaments-button"
      >
        My tournaments
      </button>
      <button id="btn-play" type="button" class="btn btn-primary"
        onclick="window.location='#add-tournament';" data-i18n-key="create-tournament-button"
      >
        Create tournament
      </button>
    </div>
  </div>
  <div class="container-fluid main-game scroll-on mt-3">
    <div id="tournament-table-container" class="static-list"></div>
  </div>
`;

const swap = (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "tournament-table-container");
    return;
  }

  const swapContainer = document.getElementById("tournament-table-container");
  swapContainer.innerHTML = response;
};

const getAllTournaments = async () => {
  await gameService.allTournaments().then(swap);
};

const allTournamentsHashChangeHandler = async () => {
  window.removeEventListener(
    CustomEvents.LANGUAGE_CHANGE_EVENT,
    getAllTournaments
  );
  window.removeEventListener("hashchange", allTournamentsHashChangeHandler);
};

const start = async (user) => {
  getAllTournaments();

  window.addEventListener(
    CustomEvents.LANGUAGE_CHANGE_EVENT,
    getAllTournaments
  );

  window.addEventListener("hashchange", allTournamentsHashChangeHandler);
};

export default new TournamentsView(html, start);
