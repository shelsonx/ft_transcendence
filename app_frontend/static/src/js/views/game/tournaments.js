import BaseLoggedView from '../baseLoggedView.js';
import gameService from '../../services/gameService.js';


class TournamentsView extends BaseLoggedView {
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

let tournamentsRows = document.getElementsByClassName("tournament-row");

const swap = (response) => {
  const swapContainer = document.getElementById("swap-container");
  swapContainer.innerHTML = response;

  tournamentsRows = document.getElementsByClassName("tournament-row");
  tournamentsRows.array.forEach(match => {
    match.addEventListener("click", () => {
      // check if we do this without changing route because we gonna need to
      window.location = '#tournament';
    })
  });
}

const start = async (user) => {
  gameService.userTournaments().then(swap);

  // const tbody = document.getElementsByTagName("tbody");
  // tbody.className = "main";
}

export default new TournamentsView(html, start);
