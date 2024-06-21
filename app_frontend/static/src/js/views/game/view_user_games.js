import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { loadErrorMessage, pageNotFoundMessage } from "../../utils/errors.js";

class SeeUserGamesView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div id="game-table-container" class="container-fluid"></div>
  <div id="message" class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
  </div>
`;

const swap = (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "message");
    return;
  }

  const swapContainer = document.getElementById("game-table-container");
  swapContainer.innerHTML = response;
};

const start = async (user) => {
  const userId = new URLSearchParams(window.location.search).get("user");

  if (userId === null) {
    pageNotFoundMessage("message");
    return;
  }

  await gameService.viewUserGames(userId).then(swap);
};

export default new SeeUserGamesView(html, start);
