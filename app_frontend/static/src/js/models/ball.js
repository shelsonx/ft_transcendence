import { BALL_VELOCITY, PONG_BALL_SIZE } from "../constants/game.js";

export default class PongBall {
  constructor(x, y, gameWidth, gameHeight) {
    this.gameWidth = gameWidth;
    this.gameHeight = gameHeight;
    this.position = {
      x,
      y,
    };
    this.velocity = {
      x: x > gameWidth / 2 ? -BALL_VELOCITY : BALL_VELOCITY,
      y: y > gameHeight / 2 ? -BALL_VELOCITY : BALL_VELOCITY,
    };
    this.size = PONG_BALL_SIZE;
  }

  draw(ctx) {
    ctx.fillStyle = "#99c9ff";
    ctx.fillRect(this.position.x, this.position.y, this.size, this.size);
  }

  update() {
    if (this.position.x + this.velocity.x > this.gameWidth) {
      this.velocity.x *= -1;
    }
    else if (this.position.x + this.velocity.x < 0) {
      this.velocity.x *= -1;
    }
    if (this.position.y + this.velocity.y > this.gameHeight) {
      this.velocity.y *= -1;
    }
    else if (this.position.y + this.velocity.y < 0) {
      this.velocity.y *= -1;
    }

    this.position.x += this.velocity.x;
    this.position.y += this.velocity.y;
  }
}
