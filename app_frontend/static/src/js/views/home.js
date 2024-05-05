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
  <div id="swap-container" class="container-fluid main"></div>
`

const swap = (response) => {
  const swapContainer = document.getElementById("swap-container");
  swapContainer.innerHTML = response;
}

const start = async () => {
  gameService.allGames().then(swap);

  // const tbody = document.getElementsByTagName("tbody");
  // tbody.className = "main";
}

export default new HomeView(html, start);
