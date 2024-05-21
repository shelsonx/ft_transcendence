import { CANVAS_WIDTH, CANVAS_HEIGHT } from "../constants/game.js";

class PongBall {
  constructor(x, y, width, height) {
    this.position = {
      x,
      y,
    };
    this.velocity = {
      x: x > CANVAS_WIDTH / 2 ? -1 : 1,
      y: y > CANVAS_HEIGHT / 2 ? -1 : 1,
    };
    this.width = width;
    this.height = height;
  }

  draw(ctx) {
    ctx.fillStyle = "#99c9ff";
    ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
  }

  update(ctx) {
    if (this.position.x + this.velocity.x > CANVAS_WIDTH) {
      this.velocity.x *= -1;
    }
    else if (this.position.x + this.velocity.x < 0) {
      this.velocity.x *= -1;
    }
    if (this.position.y + this.velocity.y > CANVAS_HEIGHT) {
      this.velocity.y *= -1;
    }
    else if (this.position.y + this.velocity.y < 0) {
      this.velocity.y *= -1;
    }

    this.position.x += this.velocity.x;
    this.position.y += this.velocity.y;
    this.draw(ctx);
  }
}

export default PongBall;
