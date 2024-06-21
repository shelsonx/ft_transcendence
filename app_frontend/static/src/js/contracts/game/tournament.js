import { objValidation as validateObj } from "../validation/objValidation.js";
import { GameRules } from "./gameRule.js";

class TournamentType {
  static CHALLENGE = "0";
  static ROUND_ROBIN = "1";
  static tournamentTypes = [
    TournamentType.CHALLENGE,
    TournamentType.ROUND_ROBIN,
  ];

  constructor(value = TournamentType.ROUND_ROBIN) {
    if (!TournamentType.tournamentTypes.includes(value)) {
      throw new Error(
        `Invalid tournament type: ${value}.
        Valid types are: ${TournamentType.tournamentTypes}`
      );
    }
    this.value = value;
  }
}

class TournamentStatus {
  static INVITATION = 0;
  static SCHEDULED = 1;
  static ON_GOING = 2;
  static ENDED = 3;
  static CANCELED = 4;
  static statusTypes = [
    TournamentStatus.INVITATION,
    TournamentStatus.SCHEDULED,
    TournamentStatus.ON_GOING,
    TournamentStatus.ENDED,
    TournamentStatus.CANCELED,
  ];

  constructor(value = TournamentStatus.INVITATION) {
    if (!TournamentStatus.statusTypes.includes(value)) {
      throw new Error(
        `Invalid tournament status: ${value}.
        Valid status types are: ${TournamentStatus.statusTypes}`
      );
    }
    this.value = value;
  }
}

class Tournament {
  static mustHaveKeys = [
    "id",
    "tournament_type",
    "status",
    "tournament_date",
    "rules",
    "number_of_players",
    "number_of_rounds",
    "players",
  ];

  constructor(
    id,
    type,
    status,
    date,
    rules,
    number_of_players,
    number_of_rounds,
    players
  ) {
    this.id = id;
    this.type = new TournamentType(type);
    this.status = new TournamentStatus(status);
    this.date = date;
    this.rules = GameRules.createGameRulesFromObj(rules);
    this.number_of_players = number_of_players;
    this.number_of_rounds = number_of_rounds;
    this.players = players;
    // this.players = GamePlayer.createGamePlayerFromObj(player_left);
  }

  static createGameFromObj(obj) {
    validateObj(Game, obj);
    return new Game(
      obj.id,
      obj.tournament_type,
      obj.status,
      new Date(obj.tournament_date),
      obj.rules,
      obj.number_of_players,
      obj.number_of_rounds,
      obj.players
    );
  }

  toJSON() {
    return {
      id: this.id,
      tournament_type: this.type.value,
      status: this.status.value,
      tournament_date: this.date.toISOString(),
      rules: this.rules.toJSON(),
      number_of_players: this.number_of_players,
      number_of_rounds: this.number_of_rounds,
      players: this.players,
      // players: this.players.toJSON(),
    };
  }
}

export { TournamentType, TournamentStatus, Tournament };
