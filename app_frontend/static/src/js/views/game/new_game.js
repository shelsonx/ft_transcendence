import BaseLoggedView from '../baseLoggedView.js';
import gameService from '../../services/gameService.js';

class NewGameView extends BaseLoggedView {
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
  <div id="add-game" class="row justify-content-center">
    <button class="btn btn-primary col-3" id="button">
      Let's play pong!
    </button>
  </div>
`

let idTarget = "swap-container";

const swap = (response) => {
  const add_game = document.getElementById(idTarget)
  // console.log(response)
  // const headers = await response.headers
  // console.log(...headers)
  // console.log(response.body)
  add_game.innerHTML = response
  // test.innerHTML = await response.text()
}

const start = async () => {
  gameService.getFormGame().then(swap);
  console.log('Pong Game View');

  const button = document.getElementById("button");
  button.addEventListener("click", () => {
    idTarget = "add-game";
    gameService.getFormGame().then(swap);
  })

}

export default new NewGameView(html, start);
