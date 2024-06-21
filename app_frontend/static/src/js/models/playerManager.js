import {
  PLAYER_COLOR,
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
      y: 0,
    };
  }

  draw(ctx) {
    ctx.fillStyle = PLAYER_COLOR;
    ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
  }

  update() {
    this.position.y += this.velocity.y;
    if (this.position.y < 0)
      this.position.y = 0;
    if (this.position.y + this.height > this.gameHeight)
      this.position.y = this.gameHeight - this.height;
  }

  resize(newGameHeight) {
    this.gameHeight = newGameHeight;
    this.width = proportionalWidth(PLAYER_WIDTH);
    this.height = proportionalHeight(PLAYER_HEIGHT);
  }
}

export default PlayerManager;
