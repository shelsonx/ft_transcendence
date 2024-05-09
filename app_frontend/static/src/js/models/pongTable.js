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
  }
}

export default PongTable;
