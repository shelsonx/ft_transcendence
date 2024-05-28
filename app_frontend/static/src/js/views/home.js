import BaseLoggedView from './baseLoggedView.js';
import gameService from '../services/gameService.js';

class HomeView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start
    },
  );
  }
}

const html = /*html*/`
  <h1>Hello, user!</h1>
  <div id="swap-container" class="container-fluid main"></div>
`

const swap = (response) => {
  // TODO: lidar quando retornar erro ou não responder
  const swapContainer = document.getElementById("swap-container");
  swapContainer.innerHTML = response;
}

const start = async () => {
  await gameService.userGames().then(swap);
}

export default new HomeView(html, start);
