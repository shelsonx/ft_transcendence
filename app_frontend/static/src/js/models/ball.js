import {
  BALL_COLOR,
  BALL_MAX_ANGLE,
  BALL_VELOCITY,
  PONG_BALL_SIZE,
} from "../constants/game.js";
import { proportionalWidth } from "../utils/size.js";
import { degToRad, radToDeg, rotate, slope } from "../utils/velocity.js";

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
    let angle = Math.random() * degToRad(BALL_MAX_ANGLE);
    if (angle === 0) angle = degToRad(BALL_MAX_ANGLE);
    const vx = Math.cos(angle) * BALL_VELOCITY;
    const vy = Math.sin(angle) * BALL_VELOCITY;

    this.velocity = {
      x: this.position.x > this.gameWidth / 2 ? -vx : vx,
      y: this.position.y > this.gameHeight / 2 ? -vy : vy,
    };
  }

  updateVelocityDueToColision(player) {
    // this.velocity.x *= -1;
    const factor =
      Math.abs(this.position.y - player.position.y) / player.height;

    if (factor >= 0.45 && factor <= 0.55) {
      // decrease the slope
      if (this.velocity.y > BALL_VELOCITY / 2) this.velocity.y *= 0.8;
      // slow down
      if (this.velocity.x > BALL_VELOCITY / 2) this.velocity.x *= 0.9;
    }
    if (factor >= 0.9 || factor <= 0.1) {
      // increase the slope
      if (this.velocity.y < 5) this.velocity.y *= 1.3;
      // speed up
      if (this.velocity.x < 3) this.velocity.x *= 1.2;
    }

    const rotateAngle = this.getVelocityRotateAngle();
    this.velocity = rotate(this.velocity, rotateAngle);
  }

  getVelocityRotateAngle() {
    const oldAngle = radToDeg(slope(this.velocity));
    let newAngle = 180 - oldAngle;

    if (newAngle < 0) newAngle += 360;
    return degToRad(newAngle - oldAngle);
  }

  resize(newGameWidth, newGameHeight) {
    this.size = proportionalWidth(PONG_BALL_SIZE);
    this.position.x = (this.position.x * newGameWidth) / this.gameWidth;
    this.position.y = (this.position.y * newGameHeight) / this.gameHeight;
    this.gameWidth = newGameWidth;
    this.gameHeight = newGameHeight;
  }
}
