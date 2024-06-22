import { objValidation as validateObj } from "../validation/objValidation.js";
import { GameRules } from "./gameRule.js";
import { GamePlayer } from "./gamePlayer.js";

class GameStatus {
  static PENDING = 0;
  static TOURNAMENT = 1;
  static SCHEDULED = 2;
  static ONGOING = 3;
  static PAUSED = 4;
  static ENDED = 5;
  static CANCELED = 6;
  static statusTypes = [
    GameStatus.PENDING,
    GameStatus.TOURNAMENT,
    GameStatus.SCHEDULED,
    GameStatus.ONGOING,
    GameStatus.PAUSED,
    GameStatus.ENDED,
    GameStatus.CANCELED,
  ];

  constructor(value = GameStatus.PENDING) {
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
    "tournament",
  ];

  constructor(
    id,
    game_datetime,
    status,
    duration,
    rules,
    player_left,
    player_right,
    tournament
  ) {
    this.id = id;
    this.game_datetime = game_datetime;
    this.status = new GameStatus(status);
    this.duration = duration;
    this.rules = GameRules.createGameRulesFromObj(rules);
    this.player_left = GamePlayer.createGamePlayerFromObj(player_left);
    this.player_right = GamePlayer.createGamePlayerFromObj(player_right);
    this.tournament = tournament;
  }

  static createGameFromObj(obj) {
    validateObj(Game, obj);
    return new Game(
      obj.id,
      new Date(obj.game_datetime),
      obj.status,
      obj.duration,
      obj.rules,
      obj.player_left,
      obj.player_right,
      obj.tournament
    );
  }

  toJSON() {
    return {
      id: this.id,
      game_datetime: this.game_datetime.toISOString(),
      status: this.status.value,
      duration: this.duration,
      rules: this.rules.toJSON(),
      player_left: this.player_left.toJSON(),
      player_right: this.player_right.toJSON(),
      tournament: this.tournament,
    };
  }
}

export { Game, GameStatus };
