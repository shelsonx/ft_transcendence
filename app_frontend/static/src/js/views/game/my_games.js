import gameService from '../../services/gameService.js';
import BaseLoggedView from '../baseLoggedView.js';

class MyGamesView extends BaseLoggedView {
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
    <h2 id="hello-user"></h2>
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
  <div class="container-fluid main-game scroll-on mt-3">
    <div id="my-games-container" class="static-list"></div>
  </div>
`

let u = null;

const cancelGame = async (e) => {
  e.preventDefault();

  const match = e.srcElement.id.split("-").pop();
  await gameService.cancelGame(match).then((response) => {
    if (response.status !== undefined) {
      // TODO: toast erro
      return;
    }
  })
  await gameService.userGames(u.id).then(swap);
  // TODO: toast sucesso
}

const deleteGame = async (e) => {
  e.preventDefault();

  const match = e.srcElement.id.split("-").pop();
  await gameService.deleteGame(match).then((response) => {
    if (response.status !== undefined) {
      // TODO: toast erro
      return;
    }
  })
  await gameService.userGames(u.id).then(swap);
  // TODO: toast sucesso
}

const swap = (response) => {
  // TODO: lidar quando retornar erro ou não responder
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
}

const start = async (user) => {
  const helloUser = document.getElementById("hello-user");
  helloUser.innerHTML = `Hello, ${user.userName}!`;

  await gameService.userGames(user.id).then(swap);
  u = user;
}

export default new MyGamesView(html, start);
