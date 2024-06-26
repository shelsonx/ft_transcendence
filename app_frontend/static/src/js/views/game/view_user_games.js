import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { loadErrorMessage, pageNotFoundMessage } from "../../utils/errors.js";
import { hashChangeHandler } from "../../utils/hashChangeHandler.js";
import { CustomEvents } from "../../constants/custom-events.js";

class SeeUserGamesView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div id="user-games-container" class="container-fluid main-game static scroll-on "></div>
  <div id="message" class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
  </div>
`;

const swap = (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "message");
    return;
  }

  const swapContainer = document.getElementById("user-games-container");
  swapContainer.innerHTML = response;
  window.addEventListener("hashchange", hashChangeHandler);
};

const start = async (user) => {
  const userId = new URLSearchParams(window.location.search).get("user");

  if (userId === null) {
    pageNotFoundMessage("message");
    return;
  }
  window.addEventListener(CustomEvents.LANGUAGE_CHANGE_EVENT, (e) => {
    console.log(e.detail.lang);
  });
  await gameService.viewUserGames(userId).then(swap);
};

export default new SeeUserGamesView(html, start);
