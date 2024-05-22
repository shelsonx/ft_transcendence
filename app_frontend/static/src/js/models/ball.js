import { BALL_VELOCITY, PONG_BALL_SIZE } from "../constants/game.js";

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
    this.size = PONG_BALL_SIZE;
    this.velocityControl = 0;
  }

  draw(ctx) {
    ctx.fillStyle = "#99c9ff";
    ctx.fillRect(this.position.x, this.position.y, this.size, this.size);
  }

  update() {
    this.velocityControl++;
    if (this.velocityControl === 2000) {
      this.velocityControl = 0;
      this.velocity.x *= 1.25;
      this.velocity.y *= 1.25;
      console.log("change velocity");
    }

    this.position.x += this.velocity.x;
    this.position.y += this.velocity.y;
  }
}
