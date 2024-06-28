import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { loadErrorMessage } from "../../utils/errors.js";
import { CustomEvents } from "../../constants/custom-events.js";

class MyTournamentsView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div class="d-flex justify-content-between">
    <h3 id="tournament-title" data-i18n-key="your-tournaments-title">
      Your tournaments
    </h3>
    <div >
      <button id="btn-data-switch" type="button" class="btn btn-info"
        onclick="window.location='#tournaments';" data-i18n-key="all-tournaments-button"
      >
        All tournaments
      </button>
      <button id="btn-play" type="button" class="btn btn-primary"
        onclick="window.location='#add-tournament';" data-i18n-key="create-tournament-button"
      >
        Create tournament
      </button>
    </div>
  </div>
  <div class="container-fluid main-game scroll-on mt-3">
    <div id="my-tournaments-container" class="static-list"></div>
  </div>
`;

let u;

const swap = (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "my-tournaments-container");
    return;
  }

  const swapContainer = document.getElementById("my-tournaments-container");
  swapContainer.innerHTML = response;
};

const getUserTournaments = async () => {
  await gameService.userTournaments(u.id).then(swap);
};

const userTournamentsHashChangeHandler = async () => {
  window.removeEventListener(
    CustomEvents.LANGUAGE_CHANGE_EVENT,
    getUserTournaments
  );
  window.removeEventListener("hashchange", userTournamentsHashChangeHandler);
};

const start = async (user) => {
  u = user;
  getUserTournaments();

  window.addEventListener(
    CustomEvents.LANGUAGE_CHANGE_EVENT,
    getUserTournaments
  );

  window.addEventListener("hashchange", userTournamentsHashChangeHandler);
};

export default new MyTournamentsView(html, start);
