import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { GameRuleType } from "../../contracts/game/gameRule.js";
import PongManager from "../../models/pongManager.js";
import { GameStatus } from "../../contracts/game/game.js";
import { canvasHeight, canvasWidth } from "../../utils/size.js";
import { PLAYER_VELOCITY } from "../../constants/game.js";

class PongGameView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <h4 class="time d-flex justify-content-center">
    <span id="pong-time"></span>
  </h4>

  <div class="d-flex justify-content-between container-sm">
    <div>
      <span class="sm name" id="name-left"></span>
      <span class="score mx-1" id="score-left"></span>
    </div>
    <div>
      <span class="score mx-1" id="score-right"></span>
      <span class="sm name" id="name-right"></span>
    </div>
  </div>

  <div class="d-flex justify-content-center">
    <canvas id="canvas"></canvas>
  </div>

  <div id="message" class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
    <button id="start" class="btn btn-primary">Start</button>
  </div>
`;

const startMessages = [
  {
    msg: "3",
    showMsgDelay: 0,
  },
  {
    msg: "2",
    showMsgDelay: 1000,
  },
  {
    msg: "1",
    showMsgDelay: 2000,
  },
  {
    msg: "Get Ready!",
    showMsgDelay: 3000,
  },
  {
    msg: "",
    showMsgDelay: 4000,
  },
];

const loadStartMessages = () => {
  const message = document.getElementById("message");

  startMessages.forEach((obj) => {
    setTimeout(() => {
      message.innerHTML = /*html*/ `
        <h1 class="game-message">
          ${obj.msg}
        </h1>
      `;
    }, obj.showMsgDelay);
  });
};

function loadEndMessage(pong) {
  const messageHtml = document.getElementById("message");
  const winner = pong.winner();
  let msg =
    winner !== null ? `${winner.user.username} won!` : "Game ended in a draw";

  if (pong.game.status.value === GameStatus.CANCELED)
    msg = "This game was cancelled";

  messageHtml.innerHTML = /*html*/ `
    <h1 class="game-message align-items-center border border-white border-opacity-10 rounded-3 form-container">
      ${msg}
    </h1>
  `;
}

const settleGame = (response) => {
  if (response.status === "not found") {
    const message = document.getElementById("message");
    message.innerHTML = /*html*/ `<h1 class="game-message">404 not Found</h1>`;
    return;
  }
  const gameObj = response.data.game;

  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = canvasWidth();
  canvas.height = canvasHeight();

  const pong = new PongManager(gameObj, canvas.width, canvas.height);
  pong.table.draw(ctx);
  pong.player_left.draw(ctx);
  pong.player_right.draw(ctx);

  if ([GameStatus.ENDED, GameStatus.CANCELED].includes(pong.game.status.value))
    return loadEndMessage(pong);

  let animationFrame;
  function animate() {
    if (pong.checkGameEnded() === true) {
      loadEndMessage(pong);
      pong.end();
      // save in back
      // window.cancelAnimationFrame(animationFrame);
    } else {
      pong.update();
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      pong.draw(ctx);
      animationFrame = requestAnimationFrame(animate);
    }
  }

  const startButton = document.getElementById("start");
  startButton.addEventListener("click", (e) => {
    loadStartMessages();
    setTimeout(() => {
      pong.begin();
      animate();
    }, startMessages[4].showMsgDelay);

    window.addEventListener("keydown", (e) => {
      e.preventDefault();
      switch (e.code) {
        case "ArrowUp":
          pong.player_right.velocity.y = -PLAYER_VELOCITY;
          break;
        case "ArrowDown":
          pong.player_right.velocity.y = PLAYER_VELOCITY;
          break;
        case "KeyW":
          pong.player_left.velocity.y = -PLAYER_VELOCITY;
          break;
        case "KeyS":
          pong.player_left.velocity.y = PLAYER_VELOCITY;
          break;
      }
    });
    window.addEventListener("keyup", (e) => {
      switch (e.code) {
        case "ArrowUp":
        case "ArrowDown":
          pong.player_right.velocity.y = 0;
          break;
        case "KeyW":
        case "KeyS":
          pong.player_left.velocity.y = 0;
          break;
      }
    });
  });

  window.addEventListener("resize", (e) => {
    canvas.width = canvasWidth();
    canvas.height = canvasHeight();
    pong.resize(canvas.width, canvas.height);
    pong.draw(ctx);
  });
};

const start = async (user) => {
  const match = new URLSearchParams(window.location.search).get("match");

  if (match === null) {
    const message = document.getElementById("message");
    message.innerHTML = /*html*/ `
      <h1 class="game-message" data-i18n-key="page-not-found--title">
        Page not Found
      </h1>`;
    return;
  }

  await gameService.game(match).then(settleGame);
};

export default new PongGameView(html, start);
