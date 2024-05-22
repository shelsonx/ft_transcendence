import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { CANVAS_WIDTH, CANVAS_HEIGHT } from "../../constants/game.js";
import { GameRuleType } from "../../contracts/game/gameRule.js";
import PongManager from "../../models/pongManager.js";
import { GameStatus } from "../../contracts/game/game.js";

class PongGameView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div id="pong-game" class="">
    <h4 class="time d-flex justify-content-center">
      <span id="pong-time">00:00</span>
    </h4>
    <div class="d-flex justify-content-sm-center">
      <div class="mx-3">
        <span class="sm name" id="name-left">A</span>
        <span class="score" id="score-left"> 0</span>
      </div>
      <div class="mx-3">
        <span class="score" id="score-right">0</span>
        <span class="sm name" id="name-right">B</span>
      </div>
    </div>
    <div class="d-flex justify-content-center">
      <canvas id="canvas"></canvas>
    </div>
  </div>

  <div id="message" class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
    <button id="start" class="btn btn-primary">Start</button>
  </div>
`;

const gameObj = {
  id: 1,
  game_datetime: new Date(),
  status: GameStatus.SCHEDULED,
  duration: {
    minutes: 0,
    seconds: 0,
  },
  rules: {
    rule_type: GameRuleType.PLAYER_POINTS,
    points_to_win: 11,
    game_total_points: null,
    max_duration: null,
  },
  player_left: {
    user: {
      id: 1,
      username: "staff42",
    },
    score: 0,
  },
  player_right: {
    user: {
      id: 1,
      username: "student42",
    },
    score: 0,
  },
};

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
        <h1>
          ${obj.msg}
        </h1>
      `;
    }, obj.showMsgDelay);
  });
};

function loadEndMessage(game) {
  const messageHtml = document.getElementById("message");
  const winner = game.winner();
  const msg =
    winner !== null
      ? `${winner.user.username} won!`
      : "Game ended in a draw";

  messageHtml.innerHTML = /*html*/ `
    <h1 class="align-items-center border border-white border-opacity-10 rounded-3 form-container">
      ${msg}
    </h1>
  `;
}

const start = async () => {
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = CANVAS_WIDTH;
  canvas.height = CANVAS_HEIGHT;

  const pong = new PongManager(gameObj, canvas.width, canvas.height);
  pong.table.draw(ctx);
  pong.player_left.draw(ctx);
  pong.player_right.draw(ctx);

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
      switch (e.code) {
        case "ArrowUp":
          pong.player_right.update("up");
          break;
        case "ArrowDown":
          pong.player_right.update("down");
          break;
        case "KeyW":
          pong.player_left.update("up");
          break;
        case "KeyS":
          pong.player_left.update("down");
          break;
      }
    });
  });

  // window.addEventListener() // resize
};

export default new PongGameView(html, start);
