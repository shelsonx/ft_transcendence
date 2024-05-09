import { objValidation as validateObj } from "../validation/objValidation.js";

class GameRuleType {
  static PLAYER_POINTS = "0";
  static GAME_TOTAL_POINTS = "1";
  static GAME_DURATION = "2";
  static gameTypes = [
    GameRuleType.PLAYER_POINTS,
    GameRuleType.GAME_TOTAL_POINTS,
    GameRuleType.GAME_DURATION,
  ];

  constructor(value = GameRuleType.PLAYER_POINTS) {
    if (!GameRuleType.gameTypes.includes(value)) {
      throw new Error(
        `Invalid game rule type: ${value}.
        Valid rule types are: ${GameRuleType.gameTypes}`
      );
    }
    this.value = value;
  }
}

class GameRules {
  static mustHaveKeys = [
    "rule_type",
    "points_to_win",
    "game_total_points",
    "max_duration",
  ];

  constructor(
    rule_type = GameRuleType.PLAYER_POINTS,
    points_to_win = 11,
    game_total_points = null,
    max_duration = null
  ) {
    this.rule_type = new GameRuleType(rule_type);
    this.points_to_win = points_to_win;
    this.game_total_points = game_total_points;
    this.max_duration = max_duration;
  }

  static createGameRulesFromObj(obj) {
    validateObj(GameRules, obj);
    return new GameRules(
      obj.rule_type,
      obj.points_to_win,
      obj.game_total_points,
      obj.max_duration
    );
  }
}

// const obj = {
//   rule_type: GameRuleType.GAME_DURATION,
//   points_to_win: null,
//   game_total_points: null,
//   max_duration: 10,
// }
// const rule = GameRules.createGameRulesFromObj(obj);
// console.log(rule)

export { GameRules };
