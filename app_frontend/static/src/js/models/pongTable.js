class PongTable {
  constructor(x, y, width, height) {
    this.position = {
      x,
      y,
    };
    this.width = width;
    this.height = height;
    // this.width = 200;
    // this.height = proportionalSize(40);
  }

  draw(ctx) {
    ctx.fillStyle = "#000000";
    ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
    ctx.strokeStyle = "#FFFFFF";
    ctx.beginPath();
    ctx.moveTo(this.position.x + this.width / 2, this.position.y);
    ctx.lineTo(this.position.x + this.width / 2, this.height);
    ctx.stroke();
  }
}

export default PongTable;
