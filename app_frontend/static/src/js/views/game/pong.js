import BaseLoggedView from '../baseLoggedView.js';
import gameService from '../../services/gameService.js';
import { CANVAS_WIDTH, CANVAS_HEIGHT } from '../../constants/game.js';
import { GameRuleType } from '../../contracts/game/gameRule.js';
import PongManager from '../../models/pongManager.js';


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
    <h4 class="d-flex justify-content-center">00:00</h4>
    <div class="d-flex justify-content-sm-center">
      <div class="mx-3">
        <span class="sm name" id="player-left-name">A</span>
        <span class="score" id="player-left-score"> 0</span>
      </div>
      <div class="mx-3">
        <span class="score" id="player-right-score">0</span>
        <span class="sm name" id="player-right-name">B</span>
      </div>
    </div>
    <div class="d-flex justify-content-center">
      <canvas id="canvas"></canvas>
    </div>
  </div>
`

const gameObj = {
  id: 1,
  game_datetime: new Date(),
  status: "scheduled",
  duration: 0,
  rules: {
    rule_type: GameRuleType.PLAYER_POINTS,
    points_to_win: 11,
    game_total_points: null,
    max_duration: null,
  },
  player_left: {
    user: {
      id: 1,
      username: "user42",
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
}

const start = async () => {
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = CANVAS_WIDTH;
  canvas.height = CANVAS_HEIGHT;
  let animationFrame;

  const pong = new PongManager(gameObj, canvas.width, canvas.height);

  function animate() {
    if (pong.checkGameEnded() === true) {
      // save in back
      // window.cancelAnimationFrame(animationFrame);
      console.log("Ended");
    }
    else {
      pong.update();
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      pong.draw(ctx);
      animationFrame = requestAnimationFrame(animate);
    }
  }
  animate();

  window.addEventListener("keydown", (e) => {
    switch(e.code) {
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

  // window.addEventListener() // resize

}

export default new PongGameView(html, start);
