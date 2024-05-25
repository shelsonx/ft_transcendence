class PlayerManager {
  constructor(player, gameHeight, x) {
    this.user = player.user;
    this.score = player.score;
    this.gameHeight = gameHeight;
    this.width = 10;
    this.height = 40;
    this.position = {
      x: x,
      y: Math.random() * gameHeight,
    };
    this.velocity = {
      x: 0,
      y: 10,
    };
  }

  draw(ctx) {
    ctx.fillStyle = "#99c9ff";
    ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
  }

  update(move) {
    if (move == "up") {
      if (this.position.y - this.velocity.y >= 0) {
        this.position.y -= this.velocity.y;
      }
    }
    else if (move == "down") {
      if (this.position.y + this.velocity.y + this.height <= this.gameHeight) {
        this.position.y += this.velocity.y;
      }
    }
  }
}

export default PlayerManager;
