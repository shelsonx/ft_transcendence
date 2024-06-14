import BaseLoggedView from '../baseLoggedView.js';
import gameService from '../../services/gameService.js';


class TournamentDetailView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start
    },
  );
  }
}

const html = /*html*/`
<div id="tournament-container" class="container-fluid main"></div>
  <div id="add-tournament" class="row justify-content-center">
    <button class="btn btn-primary col-3" id="button">
      Create New Tournament
    </button>
  </div>
`

let idTarget = "tournament-container";

const swap = (response) => {
  const add_tournament = document.getElementById(idTarget)
  // console.log(response)
  // const headers = await response.headers
  // console.log(...headers)
  // console.log(response.body)
  add_tournament.innerHTML = response
  // test.innerHTML = await response.text()
}

const start = async (user) => {
  gameService.getFormTournament().then(swap);
  console.log('Create Tournament View');

  const button = document.getElementById("button");
  button.addEventListener("click", () => {
    idTarget = "add-tournament";
    gameService.getFormTournament().then(swap);
  })

}

export default new TournamentDetailView(html, start);
