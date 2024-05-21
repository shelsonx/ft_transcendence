import PongTable from "./pongTable.js";
import PongBall from "./ball.js";
import PlayerManager from "./playerManager.js";
import { Game } from "../contracts/game/game.js";

class PongManager {
  constructor(game, gameWidth, gameHeight) {
    this.game = Game.createGameFromObj(game);
    this.width = gameWidth;
    this.height = gameHeight;

    this.table = new PongTable(0, 0, gameWidth, gameHeight);
    this.ball = new PongBall(
      Math.random() * gameWidth,
      Math.random() * gameHeight,
      gameWidth,
      gameHeight,
    );
    this.player_left = new PlayerManager(
      this.game.player_left, gameHeight, 10
    );
    this.player_right = new PlayerManager(
      this.game.player_right, gameHeight, canvas.width - 20 // const
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
          console.log(`${player.user.username} wins: ${player.score}`)
          check = true;
        }
      })
    }

    if (game_total_points !== null) {
      if (this.player_left.score + this.player_right.score === game_total_points) {
        check = true;
      }
    }

    if (this.game.rules.max_duration !== null) {}
    return check;
  }

  update() {
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
