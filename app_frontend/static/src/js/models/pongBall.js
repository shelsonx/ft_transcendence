class PongBall {
  constructor(x, y) {
    this.position = {
      x,
      y,
    };
    this.velocity = {
      x: 0,
      y: 0,
    };
    // this.width = proportionalSize(40);
    // this.height = proportionalSize(40);
    this.width = 10;
    this.height = 10;
  }

  draw(ctx) {
    ctx.fillStyle = "#99c9ff";
    ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
  }

  update(ctx) {}
}

export default PongBall;
