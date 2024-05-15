import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import PongBall from "../../models/ball.js";
import PongTable from "../../models/pongTable.js";
import PlayerManager from "../../models/playerManager.js";
import { Game } from "../../contracts/game/game.js";
class NewGameView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
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
`;

let addGameForm;
let game;
// let gameFormSwap = document.getElementById("swap-container");
// window.addEventListener("load", () => console.log("load"));

const swapGameForm = async (response) => {
  const gameFormSwap = document.getElementById("swap-container");
  gameFormSwap.innerHTML = response;

  return document.getElementById('match-form');
};

const addGameResult = async (response) => {
  console.log(typeof response);
  if (typeof response == "string") {
    const gameFormSwap = document.getElementById("swap-container");
    gameFormSwap.innerHTML = response; // precisa adicionar o listen de novo...
  } else {
    game = Game.createGameFromObj(response);

    const element = document.getElementById("pong-game");
    element.classList.remove("d-none");
  }
  // const gameFormSwap = document.getElementById("swap-container");
  // gameFormSwap.innerHTML = response;

  // return document.getElementById("button-invite");
};

// new URLSearchParams(obj).toString();
// document.addEventListener("DOMContentLoaded", (event) => {
//   console.log("DOM fully loaded and parsed");
//   console.log(buttonInvite);
// });
// document.addEventListener("load", (event) => {
//   console.log("load event");
//   console.log(buttonInvite);
// });

const start = async () => {
  addGameForm = await gameService.getFormGame().then(swapGameForm);
  console.log(addGameForm);

  addGameForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    console.log("entrou?");

    // await gameService.addGame().then(addGameResult);

    console.log("evento");
    // gameService.getFormGame().then(swap);
  });

  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = innerWidth / 2;
  canvas.height = innerHeight / 2;

  const table = new PongTable(0, 0, canvas.width, canvas.height);
  table.draw(ctx);

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

  const player1 = new PlayerManager(10, 80);
  player1.draw(ctx);
  const player2 = new PlayerManager(canvas.width - 20, canvas.height - 80);
  player2.draw(ctx);

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
  ball.draw(ctx);
};

export default new NewGameView(html, start);
