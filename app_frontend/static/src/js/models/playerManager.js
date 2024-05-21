// import { GamePlayer } from "../contracts/game/gamePlayer.js";

class PlayerManager {
  constructor(player, gameWidth, gameHeight, x) {
    this.player = player;
    this.gameWidth = gameWidth;
    this.gameHeight = gameHeight;
    // this.states = [];
    // this.currentState = this.states[0];
    // this.width = proportionalSize(40);
    // this.height = proportionalSize(40);
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
    ctx.fillStyle = "#99c9ff"; // receber o ctx no constructor?
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
