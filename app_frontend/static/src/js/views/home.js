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

let matchesRows = document.getElementsByClassName("match-row");

const swap = (response) => {
  const swapContainer = document.getElementById("swap-container");
  swapContainer.innerHTML = response;

  matchesRows = document.getElementsByClassName("match-row");
  matchesRows.array.forEach(match => {
    match.addEventListener("click", () => {
      window.location = '#pong';
    })
  });
}

const start = async () => {
  gameService.userGames().then(swap);

  // const tbody = document.getElementsByTagName("tbody");
  // tbody.className = "main";
}

export default new HomeView(html, start);
