import { TABLE_COLOR, TABLE_DIVISION_COLOR } from "../constants/game.js";

class PongTable {
  constructor(x, y, width, height) {
    this.position = {
      x,
      y,
    };
    this.width = width;
    this.height = height;
  }

  draw(ctx) {
    ctx.fillStyle = TABLE_COLOR;
    ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
    ctx.strokeStyle = TABLE_DIVISION_COLOR;
    ctx.beginPath();
    ctx.moveTo(this.position.x + this.width / 2, this.position.y);
    ctx.lineTo(this.position.x + this.width / 2, this.height);
    ctx.stroke();
  }

  resize(width, height) {
    this.width = width;
    this.height = height;
  }
}

export default PongTable;
