import BaseLoggedView from '../baseLoggedView.js';
import gameService from '../../services/gameService.js';


class NewTournamentView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start
    },
  );
  }
}

const html = /*html*/ `
  <div id="swap-container" class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
  </div>
`;

let idTarget = "swap-container";

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

export default new NewTournamentView(html, start);
