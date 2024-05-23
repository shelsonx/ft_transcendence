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
    this.size = proportionalWidth(PONG_BALL_SIZE);
    this.gameWidth = gameWidth;
    this.gameHeight = gameHeight;
    this.velocityControl = 0;
    this.startVelocity();
  }

  draw(ctx) {
    ctx.fillStyle = BALL_COLOR;
    ctx.fillRect(this.position.x, this.position.y, this.size, this.size);
  }

  update() {
    this.udpadteVelocity();
    this.position.x += this.velocity.x;
    this.position.y += this.velocity.y;
  }

  udpadteVelocity() {
    this.velocityControl++;
    if (this.velocityControl === 500) {
      this.velocityControl = 0;
      this.velocity.x *= 1.2;
      this.velocity.y *= 1.1;
    }
  }

  startVelocity() {
    this.velocity = {
      x: this.position.x > this.gameWidth / 2 ? -BALL_VELOCITY : BALL_VELOCITY,
      y: this.position.y > this.gameHeight / 2 ? -BALL_VELOCITY : BALL_VELOCITY,
    };
  }

  resize(newGameWidth, newGameHeight) {
    this.size = proportionalWidth(PONG_BALL_SIZE);
    this.position.x = (this.position.x * newGameWidth) / this.gameWidth;
    this.position.y = (this.position.y * newGameHeight) / this.gameHeight;
    this.gameWidth = newGameWidth;
    this.gameHeight = newGameHeight;
  }
}
