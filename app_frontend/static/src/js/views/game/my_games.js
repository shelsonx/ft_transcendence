import gameService from "../../services/gameService.js";
import BaseLoggedView from "../baseLoggedView.js";
import { loadErrorMessage } from "../../utils/errors.js";

class MyGamesView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div class="d-flex justify-content-end pe-1">
    <div>
      <button id="btn-all-games" type="button" class="btn btn-info"
        onclick="window.location='/';"
      >
        All games
      </button>
      <button id="btn-play" type="button" class="btn btn-primary"
        onclick="window.location='#play';"
      >
        Play
      </button>
    </div>
  </div>
  <div id="my-games-container" class="container-fluid main-game static-list scroll-on mt-3">
  </div>

  <div id="error-message" class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
  </div>
`;

let u = null;

const cancelGame = async (e) => {
  e.preventDefault();

  const match = e.srcElement.id.split("-").pop();
  await gameService.cancelGame(match).then(async (response) => {
    if (response.status !== undefined) {
      loadErrorMessage(response, "error-message");
      // TODO: toast erro
      return;
    }
    await gameService.userGames(u.id).then(swap);
    // TODO: toast sucesso
  });
};

const deleteGame = async (e) => {
  e.preventDefault();

  const match = e.srcElement.id.split("-").pop();
  await gameService.deleteGame(match).then(async (response) => {
    if (response.status !== undefined) {
      loadErrorMessage(response, "error-message");
      // TODO: toast erro
      return;
    }
    await gameService.userGames(u.id).then(swap);
    // TODO: toast sucesso
  });
};

const swap = (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "error-message");
    return;
  }

  const swapContainer = document.getElementById("my-games-container");
  swapContainer.innerHTML = response;

  const cancelButtons = document.querySelectorAll(".cancel");
  cancelButtons.forEach((element) => {
    element.addEventListener("click", cancelGame);
  });

  const deleteButtons = document.querySelectorAll(".delete");
  deleteButtons.forEach((element) => {
    element.addEventListener("click", deleteGame);
  });
};

const start = async (user) => {
  await gameService.userGames(user.id).then(swap);
  u = user;
};

export default new MyGamesView(html, start);
