import PongTable from "./pongTable.js";
import PongBall from "./ball.js";
import PlayerManager from "./playerManager.js";
import { Game, GameStatus } from "../contracts/game/game.js";
import { getTimeValue } from "../utils/timeUtils.js";
import { PLAYER_WIDTH, TABLE_PADDING } from "../constants/game.js";
import { proportionalWidth } from "../utils/size.js";

class PongManager {
  constructor(game, gameWidth, gameHeight) {
    this.game = Game.createGameFromObj(game);
    this.gameWidth = gameWidth;
    this.gameHeight = gameHeight;

    this.table = new PongTable(0, 0, gameWidth, gameHeight);
    this.ball = new PongBall(
      Math.random() * gameWidth,
      Math.random() * gameHeight,
      gameWidth,
      gameHeight
    );
    this.player_left = new PlayerManager(
      this.game.player_left,
      gameHeight,
      proportionalWidth(TABLE_PADDING)
    );
    this.player_right = new PlayerManager(
      this.game.player_right,
      gameHeight,
      gameWidth - proportionalWidth(TABLE_PADDING + PLAYER_WIDTH)
    );

    this.timeHtml = document.getElementById("pong-time");
    this.leftScoreHtml = document.getElementById("score-left");
    this.rightScoreHtml = document.getElementById("score-right");
    this.setHtmlData();
  }

  begin() {
    this.game.game_datetime = new Date();
    this.game.status.value = GameStatus.ONGOING;
    // send update to back?
  }

  end() {
    const now = new Date();
    const delta = now - this.game.game_datetime;
    const minutes = Math.floor((delta % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((delta % (1000 * 60)) / 1000);

    this.game.status.value = GameStatus.ENDED;
    this.game.duration.minutes = minutes;
    this.game.duration.seconds = seconds;
    this.game.player_left.score = this.player_left.score;
    this.game.player_right.score = this.player_right.score;
  }

  checkGameEnded() {
    const points_to_win = this.game.rules.points_to_win;
    const game_total_points = this.game.rules.game_total_points;
    const players = [this.player_left, this.player_right];
    let check = false;

    if (points_to_win !== null) {
      players.forEach((player) => {
        if (player.score === points_to_win) {
          check = true;
        }
      });
    }

    if (game_total_points !== null) {
      if (
        this.player_left.score + this.player_right.score ===
        game_total_points
      ) {
        check = true;
      }
    }

    if (this.game.rules.max_duration !== null) {
    }
    return check;
  }

  checkPoint() {
    if (this.ball.position.x + this.ball.velocity.x > this.gameWidth) {
      this.player_left.score += 1;
      this.updateHtmlPoints();
      // send update to back?
      this.ball.position.x = proportionalWidth(TABLE_PADDING);
      this.ball.position.y = Math.random() * this.gameHeight;
    } else if (this.ball.position.x + this.ball.velocity.x < 0) {
      this.player_right.score += 1;
      this.updateHtmlPoints();
      // send update to back?
      this.ball.position.x =
        this.gameWidth - proportionalWidth(TABLE_PADDING) - this.ball.size;
      this.ball.position.y = Math.random() * this.gameHeight;
    }
  }

  checkBallColisionPlayerY(player) {
    if (
      this.ball.position.y + this.ball.size >= player.position.y &&
      this.ball.position.y <= player.position.y + player.height
    ) {
      this.ball.velocity.x *= -1;
    }
  }

  checkBallColision() {
    // colision in x - with players
    let ballColisionX, playerColisionX;

    // colision with player_right
    if (this.ball.velocity.x > 0) {
      ballColisionX = this.ball.position.x + this.ball.size;
      playerColisionX = this.player_right.position.x;

      if (
        ballColisionX + this.ball.velocity.x >= playerColisionX &&
        ballColisionX <= playerColisionX
      )
        this.checkBallColisionPlayerY(this.player_right);
    }

    // colision with player_left
    else if (this.ball.velocity.x < 0) {
      ballColisionX = this.ball.position.x;
      playerColisionX = this.player_left.position.x + this.player_left.width;

      if (
        ballColisionX + this.ball.velocity.x <= playerColisionX &&
        ballColisionX >= playerColisionX
      ) {
        this.checkBallColisionPlayerY(this.player_left);
      }
    }

    // colision in y
    if (
      this.ball.position.y + this.ball.velocity.y <= 0 ||
      this.ball.position.y + this.ball.size + this.ball.velocity.y >=
        this.gameHeight
    )
      this.ball.velocity.y *= -1;
  }

  winner() {
    if (this.player_left.score > this.player_right.score)
      return this.player_left;
    if (this.player_right.score > this.player_left.score)
      return this.player_right;
    return null; // a tie
  }

  update() {
    this.checkBallColision();
    this.checkPoint();
    this.ball.update();
    this.updateHtmlTime();
  }

  draw(ctx) {
    this.table.draw(ctx);
    this.ball.draw(ctx);
    this.player_left.draw(ctx);
    this.player_right.draw(ctx);
  }

  resize(newGameWidth, newGameHeight) {
    this.gameWidth = newGameWidth;
    this.gameHeight = newGameHeight;

    this.table.resize(newGameWidth, newGameHeight);
    this.ball.resize(newGameWidth, newGameHeight);
    this.player_left.resize(newGameHeight);
    this.player_right.resize(newGameHeight);
    this.player_right.position.x =
      newGameWidth - proportionalWidth(TABLE_PADDING + PLAYER_WIDTH);
  }

  setHtmlData() {
    const left_name = document.getElementById("name-left");
    const right_name = document.getElementById("name-right");

    left_name.innerText = this.player_left.user.username;
    right_name.innerText = this.player_right.user.username;
    this.timeHtml.innerText = `
      ${getTimeValue(this.game.duration.minutes)}:${getTimeValue(
      this.game.duration.seconds
    )}
    `;
    this.updateHtmlPoints();
  }

  updateHtmlTime() {
    const now = new Date().getTime();
    const delta = now - this.game.game_datetime;
    const minutes = Math.floor((delta % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((delta % (1000 * 60)) / 1000);

    this.timeHtml.innerText = `
      ${getTimeValue(minutes)}:${getTimeValue(seconds)}
    `;
  }

  updateHtmlPoints() {
    this.leftScoreHtml.innerText = this.player_left.score;
    this.rightScoreHtml.innerText = this.player_right.score;
  }
}

export default PongManager;
