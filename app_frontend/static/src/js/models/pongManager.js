import PongTable from "./pongTable";
import PongBall from "./pongBall";
import PongPlayer from "./pongPlayer";
import { Game } from "../contracts/game/game";



class PongManager extends Game {
  constructor(...args) {
    super(...args);

    this.player_left = new PongPlayer(this.player_left);
    this.player_right = new PongPlayer(this.player_right);
  }
}

export default PongManager
