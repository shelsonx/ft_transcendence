import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import gameInfoService from "../../services/gameInfoService.js";
import PongManager from "../../models/pongManager.js";
import { GameStatus } from "../../contracts/game/game.js";
import { canvasHeight, canvasWidth } from "../../utils/size.js";
import { PLAYER_VELOCITY } from "../../constants/game.js";
import { loadErrorMessage, pageNotFoundMessage } from "../../utils/errors.js";
import { hashChangeHandler } from "../../utils/hashChangeHandler.js";

class PongGameView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div class="static scroll-on" id="game-data">
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
    <div class="py-5">
      <div class="d-flex justify-content-center pb-3" id="game-buttons">
        <button id="pause" class="btn btn-primary d-none">Pause</button>
        <button id="continue" class="btn btn-primary d-none">Continue</button>
      </div>
      <div class="d-flex justify-content-center">
        <button id="back-tournament" class="btn btn-secondary d-none">Back to tournament</button>
      </div>
    </div>
  </div>

  <div id="message" class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
    <button id="start" class="btn btn-primary">Start</button>
  </div>
`;

let match = null;
let animationFrame;

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
        <h1 class="error-message">
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
    winner !== null ? `${winner.user.name} won!` : "Game ended in a draw";

  if (pong.game.status.value === GameStatus.CANCELED)
    msg = "This game was cancelled";

  messageHtml.innerHTML = /*html*/ `
    <h1 class="error-message align-items-center border border-white border-opacity-10 rounded-3 form-container">
      ${msg}
    </h1>
  `;
}

const updateUserStats = async (users) => {
  users.forEach((user) => {
    try {
      gameInfoService.updateScoresUser(user);
    } catch (error) {}
  });
};

const updateUsersPlaying = (pong, playing) => {
  const users = [pong.player_left.user.id, pong.player_right.user.id];
  users.forEach((user) => {
    try {
      const data = {
        id_msc: user,
        playing: playing,
      };
      gameInfoService.updateUserPlaying(data);
    } catch (error) {}
  });
};

const saveGame = async (pong, update = false) => {
  if (update) pong.updateToSave();
  pong.save().then((response) => {
    if (response.status !== undefined) {
      loadErrorMessage(response, "message");
      window.cancelAnimationFrame(animationFrame);
      const gameData = document.getElementById("game-data");
      gameData.classList.add("d-none");
    } else if (
      pong.game.status.value === GameStatus.ENDED &&
      response.hasOwnProperty("is_success") &&
      response.is_success === true
    ) {
      if (
        response.hasOwnProperty("data") &&
        response.data.hasOwnProperty("stats") &&
        response.data.stats !== null
      )
        updateUserStats(response.data.stats);
    }
  });
};

const settleGame = (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "message");
    return;
  }
  const gameObj = response.data.game;
  if (gameObj.status === GameStatus.PENDING) {
    window.location.replace(`?match=${match}#verify-player`);
    return;
  }
  if (gameObj.status === GameStatus.TOURNAMENT) {
    window.location.replace(`?t=${gameObj.tournament}#tournament`);
    return;
  }

  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  canvas.width = canvasWidth();
  canvas.height = canvasHeight();

  const pong = new PongManager(match, gameObj, canvas.width, canvas.height);
  pong.table.draw(ctx);
  pong.player_left.draw(ctx);
  pong.player_right.draw(ctx);

  if ([GameStatus.ENDED, GameStatus.CANCELED].includes(pong.game.status.value))
    return loadEndMessage(pong);

  const keyDownHandler = (e) => {
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
  };

  const keyUpHandler = (e) => {
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
  };

  const resizeHandler = (e) => {
    canvas.width = canvasWidth();
    canvas.height = canvasHeight();
    pong.resize(canvas.width, canvas.height);
    pong.draw(ctx);
  };

  const beforeUnloadHandler = (event) => {
    event.preventDefault();

    // Included for legacy support, e.g. Chrome/Edge < 119
    event.returnValue = true;
    if (pong.game.status.value === GameStatus.ONGOING) pauseGame();
  };

  const stopGlobalEvents = () => {
    window.cancelAnimationFrame(animationFrame);
    window.removeEventListener("keydown", keyDownHandler);
    window.removeEventListener("keyup", keyUpHandler);
    window.removeEventListener("resize", resizeHandler);
    window.removeEventListener("beforeunload", beforeUnloadHandler);
  };

  const initGlobalEvents = () => {
    window.addEventListener("keydown", keyDownHandler);
    window.addEventListener("keyup", keyUpHandler);
    window.addEventListener("resize", resizeHandler);
    window.addEventListener("beforeunload", beforeUnloadHandler);
  };

  function animate() {
    const scored_point = pong.update();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    pong.draw(ctx);

    if (pong.checkGameEnded() === true) {
      pong.end();
      stopGlobalEvents();
      loadEndMessage(pong);
      const gameButtons = document.getElementById("game-buttons");
      gameButtons.classList.add("d-none");
      updateTournamentBtn();
      saveGame(pong);
      updateUsersPlaying(pong, false);
    } else {
      if (scored_point === true) saveGame(pong, true);
      animationFrame = requestAnimationFrame(animate);
    }
  }

  const startButton = document.getElementById("start");
  const pauseButton = document.getElementById("pause");
  const continueButton = document.getElementById("continue");
  const tournamentButton = document.getElementById("back-tournament");

  const updateTournamentBtn = () => {
    if (pong.game.tournament !== null) {
      tournamentButton.classList.remove("d-none");
    }
  }
  updateTournamentBtn();

  const startGame = (e) => {
    loadStartMessages();

    setTimeout(() => {
      if (pong.game.status.value === GameStatus.SCHEDULED) pong.begin();
      else pong.continue();
      animate();
      pauseButton.classList.remove("d-none");
      tournamentButton.classList.add("d-none");
      saveGame(pong);
      updateUsersPlaying(pong, true);
    }, startMessages[4].showMsgDelay);

    initGlobalEvents();
  };

  const pauseGame = () => {
    pong.pause();
    stopGlobalEvents();
    pauseButton.classList.add("d-none");
    continueButton.classList.remove("d-none");
    updateTournamentBtn();
    saveGame(pong);
    updateUsersPlaying(pong, false);
  };

  const continueGame = () => {
    window.cancelAnimationFrame(animationFrame);
    continueButton.classList.add("d-none");
    pauseButton.classList.remove("d-none");
    tournamentButton.classList.add("d-none");
    pong.continue();
    animate();
    initGlobalEvents();
    saveGame(pong);
    updateUsersPlaying(pong, true);
  };

  const goToTournament = () => {
    window.location.href = "?t=" + pong.game.tournament + "#tournament";
  }

  startButton.addEventListener("click", startGame);
  pauseButton.addEventListener("click", pauseGame);
  continueButton.addEventListener("click", continueGame);
  tournamentButton.addEventListener("click", goToTournament);

  const pongHashChangeHandler = (e) => {
    hashChangeHandler();
    if (pong.game.status.value === GameStatus.ONGOING) pauseGame();
  };
  window.addEventListener("hashchange", pongHashChangeHandler);

  const visibilityChangeHandler = (e) => {
    if (document.hidden) {
      if (pong.game.status.value === GameStatus.ONGOING) pauseGame();
    }
  };
  document.addEventListener("visibilitychange", visibilityChangeHandler);
};

const start = async (user) => {
  match = new URLSearchParams(window.location.search).get("match");

  if (match === null) {
    pageNotFoundMessage("message");
    return;
  }

  await gameService.game(match).then(settleGame);
};

export default new PongGameView(html, start);
