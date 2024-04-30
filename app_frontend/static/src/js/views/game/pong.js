import BaseLoggedView from '../baseLoggedView.js';
import gameService from '../../services/gameService.js';

class PongGameView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start
    },
  );
  }
}

const html = /*html*/`
  <h1 class="text-bg-dark">Play pong view</h1>
  <div id="test"></div>
  <button class="btn btn-primary" id="button">Click me</button>
`

const swap = async (response) => {
  const test = document.getElementById("test")
  // console.log(response)
  // const headers = await response.headers
  // console.log(...headers)
  // console.log(response.body)
  test.innerHTML += await response.text()
  // test.innerHTML = await response.text()
}

const start = async () => {
  gameService.gameTest().then(swap);
  console.log('Pong Game View');

  const button = document.getElementById("button");
  button.addEventListener("click", () => {
    gameService.gameTest().then(swap);
  })
}

export default new PongGameView(html, start);
