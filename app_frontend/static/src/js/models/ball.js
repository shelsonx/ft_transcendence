import {
  BALL_COLOR,
  BALL_VELOCITY,
  PONG_BALL_SIZE,
} from "../constants/game.js";
import { proportionalWidth } from "../utils/size.js";

export default class PongBall {
  constructor(x, y, gameWidth, gameHeight) {
    this.position = {
      x,
      y,
    };
    this.velocity = {
      x: x > gameWidth / 2 ? -BALL_VELOCITY : BALL_VELOCITY,
      y: y > gameHeight / 2 ? -BALL_VELOCITY : BALL_VELOCITY,
    };
    this.size = proportionalWidth(PONG_BALL_SIZE);
    this.velocityControl = 0;
    this.gameWidth = gameWidth;
    this.gameHeight = gameHeight;
  }

  draw(ctx) {
    ctx.fillStyle = BALL_COLOR;
    ctx.fillRect(this.position.x, this.position.y, this.size, this.size);
  }

  update() {
    this.velocityControl++;
    if (this.velocityControl === 2000) {
      this.velocityControl = 0;
      this.velocity.x *= 1.25;
      this.velocity.y *= 1.25;
    }

    this.position.x += this.velocity.x;
    this.position.y += this.velocity.y;
  }

  resize(newGameWidth, newGameHeight) {
    this.size = proportionalWidth(PONG_BALL_SIZE);
    this.position.x = this.position.x * newGameWidth / this.gameWidth;
    this.position.y = this.position.y * newGameHeight / this.gameHeight;
    this.gameWidth = newGameWidth;
    this.gameHeight = newGameHeight;
  }
}
