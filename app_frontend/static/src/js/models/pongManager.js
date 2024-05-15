import PongTable from "./pongTable";
import PongBall from "./ball";
import PlayerManager from "./playerManager";
import { Game } from "../contracts/game/game";

class PongManager extends Game {
  constructor(...args) {
    super(...args);

    this.player_left = new PlayerManager(this.player_left);
    this.player_right = new PlayerManager(this.player_right);
  }
}

export default PongManager;
