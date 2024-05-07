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
<div class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
  <div
    id="swap-container"
    class="d-flex flex-column align-items-center justify-content border border-white border-opacity-10 rounded-3 p-4 form-container"
    >

  </div>
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
  // const button = document.getElementById("button");
  // button.addEventListener("click", () => {
  //   idTarget = "add-game";
  //   gameService.getFormGame().then(swap);
  // })
}

export default new NewGameView(html, start);
