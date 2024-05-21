import PongTable from "./pongTable.js";
import PongBall from "./ball.js";
import PlayerManager from "./playerManager.js";
import { Game } from "../contracts/game/game.js";

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
    this.player_left = new PlayerManager(this.game.player_left, gameHeight, 10);
    this.player_right = new PlayerManager(
      this.game.player_right,
      gameHeight,
      canvas.width - 20 // const
    );
  }

  checkGameEnded() {
    const points_to_win = this.game.rules.points_to_win;
    const game_total_points = this.game.rules.game_total_points;
    const players = [this.player_left, this.player_right];
    let check = false;

    if (points_to_win !== null) {
      players.forEach((player) => {
        if (player.score === points_to_win) {
          console.log(`${player.user.username} wins: ${player.score}`);
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
      console.log(
        `${this.player_left.user.username} earns 1 point: ${this.player_left.score}`
      );
      // update score on screen
      // send update to back?
      this.ball.position.x = 0;
      this.ball.position.y = Math.random() * this.gameHeight;
    } else if (this.ball.position.x + this.ball.velocity.x < 0) {
      this.player_right.score += 1;
      console.log(
        `${this.player_right.user.username} earns 1 point: ${this.player_right.score}`
      );
      // update score on screen
      // send update to back?
      this.ball.position.x = this.gameWidth - this.ball.size * 2;
      this.ball.position.y = Math.random() * this.gameHeight;
    }
  }

  checkBallColision() {
    // colision in x - with players
    if (
      this.ball.position.x + this.ball.velocity.x ===
      this.player_right.position.x
    ) {
      if (
        this.ball.position.y >= this.player_right.position.y &&
        this.ball.position.y <=
          this.player_right.position.y + this.player_right.height
      ) {
        this.ball.velocity.x *= -1;
        console.log("player right colision detected")
      }
    } else if (
      this.ball.position.x + this.ball.velocity.x ===
      this.player_left.position.x + this.player_left.width
    ) {
      if (
        this.ball.position.y >= this.player_left.position.y &&
        this.ball.position.y <=
          this.player_left.position.y + this.player_left.height
      ) {
        this.ball.velocity.x *= -1;
        console.log("player left colision detected")
      }
    }

    // colision in y
    if (this.ball.position.y + this.ball.velocity.y > this.gameHeight) {
      this.ball.velocity.y *= -1;
    }
    else if (this.ball.position.y + this.ball.velocity.y < 0) {
      this.ball.velocity.y *= -1;
    }
  }

  update() {
    this.checkBallColision();
    this.checkPoint();
    this.ball.update();
  }

  draw(ctx) {
    this.table.draw(ctx);
    this.ball.draw(ctx);
    this.player_left.draw(ctx);
    this.player_right.draw(ctx);
  }
}

export default PongManager;
