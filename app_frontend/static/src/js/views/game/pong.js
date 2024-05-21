import BaseLoggedView from '../baseLoggedView.js';
import gameService from '../../services/gameService.js';
import PongBall from "../../models/ball.js";
import PongTable from "../../models/pongTable.js";
import PlayerManager from "../../models/playerManager.js";
import { Game } from "../../contracts/game/game.js";
import { CANVAS_WIDTH, CANVAS_HEIGHT } from '../../constants/game.js';


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
  <div id="pong-game" class="">
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

const start = async () => {
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = CANVAS_WIDTH;
  canvas.height = CANVAS_HEIGHT;

  const table = new PongTable(0, 0, canvas.width, canvas.height);
  const ball = new PongBall(
    Math.random() * canvas.width, Math.random() * canvas.height, 10, 10
  );
  // const player1 = new PlayerManager(10, 80);
  // const player2 = new PlayerManager(canvas.width - 20, canvas.height - 80);

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    table.draw(ctx);
    ball.update(ctx);
    // player1.draw(ctx);
    // player2.draw(ctx);
    requestAnimationFrame(animate);
  }
  animate();

  window.addEventListener("keydown", (e) => {
    console.log(e)
    switch(e.code) {
      case "ArrowUp":
        console.log("Right player up");
        break;
      case "ArrowDown":
        console.log("Right player down");
        break;
      case "KeyW":
        console.log("Left player up");
        break;
      case "KeyS":
        console.log("Left player down");
        break;
    }
  });

  // window.addEventListener() // resize

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

}

export default new PongGameView(html, start);
