import { objValidation as validateObj } from "../validation/objValidation.js";


class GameUser {
  static mustHaveKeys = ["id", "username"];

  constructor(id, username) {
    this.id = id;
    this.username = username;
  }

  static createGameUserFromObj(obj) {
    validateObj(GameUser, obj);
    return new GameUser(obj.id, obj.username);
  }
}

class GamePlayer {
  static mustHaveKeys = ["user", "score"];

  constructor(user, score) {
    this.user = GameUser.createGameUserFromObj(user);  // pode ser anônimo?
    this.score = score;
  }

  static createGamePlayerFromObj(obj) {
    validateObj(GamePlayer, obj);
    return new GamePlayer(obj.id, obj.username);
  }

  draw() {};
  update() {};
}

// const player = new GamePlayer()

export { GamePlayer };
