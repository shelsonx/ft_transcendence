import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";

class SeeUserGamesView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/`
  <div id="game-table-container" class="container-fluid"></div>
  <div id="message" class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
  </div>
`

const loadErrorMessage = (error) => {
  const message = document.getElementById("message");
  message.innerHTML = /*html*/ `
    <h1 class="game-message text-center">${error.status} <br> ${error.message}</h1>`;
};

const swap = (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response);
    return;
  }

  const swapContainer = document.getElementById("game-table-container");
  swapContainer.innerHTML = response;
}

const start = async (user) => {
  const userId = new URLSearchParams(window.location.search).get("user");

  if (userId === null) {
    const message = document.getElementById("message");
    message.innerHTML = /*html*/ `
      <h1 class="game-message" data-i18n-key="page-not-found--title">
        Page not Found
      </h1>`;
    return;
  }

  await gameService.viewUserGames(userId).then(swap);
};

export default new SeeUserGamesView(html, start);
