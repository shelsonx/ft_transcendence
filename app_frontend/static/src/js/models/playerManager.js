import {
  MAIN_COLOR_GAME,
  PLAYER_HEIGHT,
  PLAYER_WIDTH,
} from "../constants/game.js";
import { proportionalHeight, proportionalWidth } from "../utils/size.js";

class PlayerManager {
  constructor(player, gameHeight, x) {
    this.user = player.user;
    this.score = player.score;
    this.gameHeight = gameHeight;
    this.width = proportionalWidth(PLAYER_WIDTH);
    this.height = proportionalHeight(PLAYER_HEIGHT);
    this.position = {
      x: x,
      y: Math.random() * (gameHeight - this.height),
    };
    this.velocity = {
      x: 0,
      y: 10,
    };
  }

  draw(ctx) {
    ctx.fillStyle = MAIN_COLOR_GAME;
    ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
  }

  update(move) {
    if (move == "up") {
      if (this.position.y - this.velocity.y >= 0) {
        this.position.y -= this.velocity.y;
      }
    } else if (move == "down") {
      if (this.position.y + this.velocity.y + this.height <= this.gameHeight) {
        this.position.y += this.velocity.y;
      }
    }
  }

  resize(newGameHeight) {
    this.gameHeight = newGameHeight;
    this.width = proportionalWidth(PLAYER_WIDTH);
    this.height = proportionalHeight(PLAYER_HEIGHT);
  }
}

export default PlayerManager;
