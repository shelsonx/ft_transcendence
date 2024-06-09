import { objValidation as validateObj } from "../validation/objValidation.js";
import { GameRules } from "./gameRule.js";
import { GamePlayer } from "./gamePlayer.js";

class GameStatus {
  static PENDING = 0;
  static SCHEDULED = 1;
  static ONGOING = 2;
  static PAUSED = 3;
  static ENDED = 4;
  static CANCELED = 5;
  static statusTypes = [
    GameStatus.PENDING,
    GameStatus.SCHEDULED,
    GameStatus.ONGOING,
    GameStatus.ENDED,
    GameStatus.CANCELED,
  ];

  constructor(value = GameStatus.SCHEDULED) {
    if (!GameStatus.statusTypes.includes(value)) {
      throw new Error(
        `Invalid game status: ${value}.
        Valid status types are: ${GameStatus.statusTypes}`
      );
    }
    this.value = value;
  }
}

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
    this.status = new GameStatus(status);
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

export { Game, GameStatus };
