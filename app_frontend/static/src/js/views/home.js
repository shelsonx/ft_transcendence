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
  <div id="swap-container"></div>
`

const swap = (response) => {
  const swapContainer = document.getElementById("swap-container")
  swapContainer.innerHTML = response
}

const start = async () => {
  gameService.allGames().then(swap);
}

export default new HomeView(html, start);
