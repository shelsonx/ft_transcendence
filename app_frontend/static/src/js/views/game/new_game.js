import BaseLoggedView from '../baseLoggedView.js';
import gameService from '../../services/gameService.js';
import PongBall from '../../models/pongBall.js';
import PongTable from '../../models/pongTable.js';
import PongPlayer from '../../models/pongPlayer.js';
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
  <div id="swap-container" class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
  </div>
  <div id="pong-game" class="d-none">
    <h3 class="row justify-content-center">Duration: 00:00</h3>
    <div class="row justify-content-center">
      <div class="col">
        <h3 class="row justify-content-center">Player A</h3>
        <h2 class="row justify-content-center">0</h2>
        <!-- <p>{{ match.player_a.id_reference }}</p>
        <p>Points: {{ match.score_a }}</p> -->
      </div>
      <canvas id="canvas" class="col"></canvas>
      <div class="col">
        <h3 class="row justify-content-center">Player B</h3>
        <h2 class="row justify-content-center">0</h2>
        <!-- <p>{{ match.player_b.id_reference }}</p>
        <p>Points: {{ match.score_b }}</p> -->
      </div>
    </div>
  </div>
`

// window.addEventListener("load", () => console.log("load"));

let test = "test"
console.log("init")
console.log(test)
console.log(('b' + 'a' + + + 'a' + 'a').toLowerCase());

const handleRequest = (response) => {
  // gameFormSwap.innerHTML = response
  console.log(response);
}
const getGameForm = async (response) => {
  // console.log(response)
  // const headers = await response.headers
  // console.log(...headers)
  // console.log(response.body)
  // test.innerHTML = await response.text()
  const gameFormSwap = document.getElementById("swap-container");
  gameFormSwap.innerHTML = response
  buttonInvite = document.getElementById("button-invite");
  return buttonInvite
}



const start = async () => {
  console.log("start")
  console.log(test)
  buttonInvite = await gameService.getFormGame().then(getGameForm);

  buttonInvite.addEventListener("submit", async (e) => {
    e.preventDefault();
    const element = document.getElementById("pong-game")
    element.classList.remove('d-none');
    gameService.addGame().then(handleRequest);
    console.log("evento")
    // gameService.getFormGame().then(swap);
  })

  test = "mudou"
  console.log(test)

  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = innerWidth / 2;
  canvas.height = innerHeight / 2;

  const table = new PongTable(0, 0, canvas.width, canvas.height);
  table.draw()


  // class PongPlayer {
  //   constructor(x, y) {
  //     this.position = {
  //       x,
  //       y,
  //     };
  //     this.velocity = {
  //       x: 0,
  //       y: 0,
  //     };
  //     // this.width = proportionalSize(40);
  //     // this.height = proportionalSize(40);
  //     this.width = 10;
  //     this.height = 40;
  //   }
  //   draw() {
  //     ctx.fillStyle = "#99c9ff";
  //     ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
  //   }
  // }

  const player1 = new PongPlayer(10, 80);
  player1.draw()
  const player2 = new PongPlayer(canvas.width - 20, canvas.height - 80);
  player2.draw()

  // class PongBall {
  //   constructor(x, y) {
  //     this.position = {
  //       x,
  //       y,
  //     };
  //     this.velocity = {
  //       x: 0,
  //       y: 0,
  //     };
  //     // this.width = proportionalSize(40);
  //     // this.height = proportionalSize(40);
  //     this.width = 10;
  //     this.height = 10;
  //   }
  //   draw() {
  //     ctx.fillStyle = "#99c9ff";
  //     ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
  //   }
  // }

  const ball = new PongBall(canvas.width / 2, canvas.height / 2);
  ball.draw()
}

let gameFormSwap = document.getElementById("swap-container");
let buttonInvite;

export default new NewGameView(html, start);
