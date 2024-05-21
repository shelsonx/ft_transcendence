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
      y: 0,
    };
  }

  draw(ctx) {
    ctx.fillStyle = "#99c9ff"; // receber o ctx no constructor?
    ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
  }

  update(ctx) {
    this.draw(ctx);
    // this.position.x += this.velocity.x;
    // this.position.y += this.velocity.y;

    // if (this.position.y + this.height + this.velocity.y <= canvas.height) {
    //   if (this.position.y < 0) {
    //     this.position.y = 0;
    //     this.velocity.y = gravity;
    //   }
    //   this.velocity.y += gravity;
    // } else {
    //   this.velocity.y = 0;
    // }

    // if (this.position.x < this.width) {
    //   this.position.x = this.width;
    // }

    // if (this.position.x >= canvas.width - 2 * this.width) {
    //   this.position.x = canvas.width - 2 * this.width;
    // }
  }
}

export default PlayerManager;
