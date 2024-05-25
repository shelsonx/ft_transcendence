import { objValidation as validateObj } from "../validation/objValidation.js";
import { GameRules } from "./gameRule.js";
import { GamePlayer } from "./gamePlayer.js";


class Game {
  static mustHaveKeys = [
    "id",
    "game_datetime",
    "status",
    "duration",
    "rules",
    "player_left",
    "player_right",
  ];

  constructor(
    id,
    game_datetime,
    status,
    duration,
    rules,
    player_left,
    player_right
  ) {
    this.id = id;
    this.game_datetime = game_datetime;
    this.status = status;
    this.duration = duration;
    this.rules = GameRules.createGameRulesFromObj(rules);
    this.player_left = GamePlayer.createGamePlayerFromObj(player_left);
    this.player_right = GamePlayer.createGamePlayerFromObj(player_right);
  }

  static createGameFromObj(obj) {
    validateObj(Game, obj);
    return new Game(
      obj.id,
      obj.game_datetime,
      obj.status,
      obj.duration,
      obj.rules,
      obj.player_left,
      obj.player_right
    );
  }
}

export { Game };
