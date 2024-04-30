import BaseLoggedView from '../baseLoggedView.js';
import gameService from '../../services/gameService.js';
// import Player from './player.js'
// import PongTable from './table.js';


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

  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = innerWidth / 2;
  canvas.height = innerHeight / 2;

  class PongTable {
    constructor() {
      this.position = {
        x: 0,
        y: 0,
      };
      this.width = canvas.width;
      this.height = canvas.height;
    }
    draw() {
      ctx.fillStyle = "#000000";
      ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
    }
  }

  const table = new PongTable();
  table.draw()

  class PongPlayer {
    constructor(x, y) {
      this.position = {
        x,
        y,
      };
      this.velocity = {
        x: 0,
        y: 0,
      };
      // this.width = proportionalSize(40);
      // this.height = proportionalSize(40);
      this.width = 10;
      this.height = 40;
    }
    draw() {
      ctx.fillStyle = "#99c9ff";
      ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
    }
  }

  const player1 = new PongPlayer(10, 80);
  player1.draw()
  const player2 = new PongPlayer(canvas.width - 20, canvas.height - 80);
  player2.draw()

  class PongBall {
    constructor(x, y) {
      this.position = {
        x,
        y,
      };
      this.velocity = {
        x: 0,
        y: 0,
      };
      // this.width = proportionalSize(40);
      // this.height = proportionalSize(40);
      this.width = 10;
      this.height = 10;
    }
    draw() {
      ctx.fillStyle = "#99c9ff";
      ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
    }
  }

  const ball = new PongBall(canvas.width / 2, canvas.height / 2);
  ball.draw()
}

export default new PongGameView(html, start);
