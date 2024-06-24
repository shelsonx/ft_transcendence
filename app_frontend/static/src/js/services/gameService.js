import { VerificationType } from "../contracts/game/validation.js";
import { getFrontErrorMessage } from "../utils/errors.js";
import authService from "./authService.js";
import { HttpClient, HttpClientRequestData } from "./httpClient.js";

class GameService {
  constructor() {
    this.baseUrl = "https://localhost:8020";
    this.httpClient = new HttpClient(this.baseUrl, false);
    this.user = null;
  }

  async handleResponse(requestData) {
    try {
      const response = await this.httpClient.makeRequest(requestData);
      return response;
    } catch (error) {
      error.message = getFrontErrorMessage(error.status);
      if (error.status === undefined) error.status = 500;
      return error;
    }
  }

  async updateUser(id, formData) {
    const data = {
      username: formData.get("username"),
      avatar: formData.get("avatar"),
    };
    const requestData = new HttpClientRequestData("PATCH", `/game/${id}`, data);
    requestData.headers["Content-Type"] = "default";
    const response = await this.handleResponse(requestData);
    return response;
  }

  async allGames() {
    const requestData = new HttpClientRequestData("GET", "/games");
    const response = await this.handleResponse(requestData);
    return response;
  }

  async userGames(id) {
    const requestData = new HttpClientRequestData("GET", `/user-games/${id}`);
    const response = await this.handleResponse(requestData);
    return response;
  }

  async viewUserGames(id) {
    const requestData = new HttpClientRequestData(
      "GET",
      `/view-user-games/${id}`
    );
    const response = await this.handleResponse(requestData);
    return response;
  }

  async getFormGame() {
    const requestData = new HttpClientRequestData("GET", "/game");
    const response = await this.handleResponse(requestData);
    return response;
  }

  async addGame(formData) {
    const data = {
      username: formData.get("username"),
      rule_type: formData.get("rule_type"),
      points_to_win: formData.get("points_to_win"),
      game_total_points: formData.get("game_total_points"),
      max_duration: formData.get("max_duration"),
    };
    const requestData = new HttpClientRequestData("POST", "/game", data);
    requestData.headers["Content-Type"] = "application/x-www-form-urlencoded";
    const response = await this.handleResponse(requestData);
    return response;
  }

  async game(id) {
    const requestData = new HttpClientRequestData("GET", `/game/${id}`);
    const response = await this.handleResponse(requestData);
    return response;
  }

  async updateGame(id, game) {
    const data = game.toJSON();
    const requestData = new HttpClientRequestData("PATCH", `/game/${id}`, data);
    requestData.headers["Content-Type"] = "default";
    const response = await this.handleResponse(requestData);
    return response;
  }

  async validateGameForm(id) {
    const requestData = new HttpClientRequestData(
      "GET",
      `/game-validation/${id}`
    );
    const response = await this.handleResponse(requestData);
    return response;
  }

  async validateGame(id, formData) {
    const auth_data = {
      code_user_receiver_id: {
        [formData.get("token")]: formData.get("user"),
      },
      user_requester_id: this.user.id,
      game_id: id,
      game_type: VerificationType.GAME,
    };

    let auth_response = null;
    try {
      auth_response = await authService.validateGame2Factor(auth_data);
    } catch (error) {
      if (error.status === 400 && error.message === "Invalid Access Token") {
        auth_response = {
          status: error.status,
          is_success: false,
          error: error.message,
        };
      } else {
        error.message = getFrontErrorMessage(error.status);
        if (error.status === undefined) error.status = 500;
        return error;
      }
    }

    const data = {
      user: formData.get("user"),
      token: formData.get("token"),
      auth_data: auth_response,
    };
    const requestData = new HttpClientRequestData(
      "PATCH",
      `/game-validation/${id}`,
      data
    );
    requestData.headers["Content-Type"] = "default";

    const response = await this.handleResponse(requestData);
    return response;
  }

  async cancelGame(id) {
    const requestData = new HttpClientRequestData("PUT", `/game/${id}`);
    requestData.headers["Content-Type"] = "application/x-www-form-urlencoded";
    const response = await this.handleResponse(requestData);
    return response;
  }

  async deleteGame(id) {
    const requestData = new HttpClientRequestData("DELETE", `/game/${id}`);
    const response = await this.handleResponse(requestData);
    return response;
  }

  async allTournaments() {
    const requestData = new HttpClientRequestData("GET", "/tournaments");
    const response = await this.handleResponse(requestData);
    return response;
  }

  async userTournaments(id) {
    const requestData = new HttpClientRequestData("GET", `/tournaments/${id}`);
    const response = await this.handleResponse(requestData);
    return response;
  }

  async getFormTournament() {
    const requestData = new HttpClientRequestData("GET", "/tournament");
    const response = await this.handleResponse(requestData);
    return response;
  }

  async addTournament(formData) {
    const data = {
      rule_type: formData.get("rule_type"),
      points_to_win: formData.get("points_to_win"),
      game_total_points: formData.get("game_total_points"),
      max_duration: formData.get("max_duration"),
      name: formData.get("name"),
      tournament_type: formData.get("tournament_type"),
      number_of_players: formData.get("number_of_players"),
      number_of_rounds: formData.get("number_of_rounds"),
      username: formData.getAll("username"),
      alias_name: formData.getAll("alias_name"),
    };
    const requestData = new HttpClientRequestData("POST", "/tournament", data);
    requestData.headers["Content-Type"] = "application/x-www-form-urlencoded";
    const response = await this.handleResponse(requestData);
    return response;
  }

  async tournament(id) {
    const requestData = new HttpClientRequestData("GET", `/tournament/${id}`);
    const response = await this.handleResponse(requestData);
    return response;
  }

  async cancelTournament(id) {
    const requestData = new HttpClientRequestData("PUT", `/tournament/${id}`);
    requestData.headers["Content-Type"] = "application/x-www-form-urlencoded";
    const response = await this.handleResponse(requestData);
    return response;
  }

  async deleteTournament(id) {
    const requestData = new HttpClientRequestData(
      "DELETE",
      `/tournament/${id}`
    );
    const response = await this.handleResponse(requestData);
    return response;
  }

  async validateTournamentForm(id) {
    const requestData = new HttpClientRequestData(
      "GET",
      `/tournament-validation/${id}`
    );
    const response = await this.handleResponse(requestData);
    return response;
  }

  async validateTournament(id, player_id, formData) {
    const auth_data = {
      code_user_receiver_id: {
        [formData.get("token")]: formData.get("user"),
      },
      user_requester_id: this.user.id,
      game_id: id,
      game_type: VerificationType.GAME,
    };

    let auth_response = null;
    try {
      auth_response = await authService.validateGame2Factor(auth_data);
    } catch (error) {
      if (error.status === 400 && error.message === "Invalid Access Token") {
        auth_response = {
          status: error.status,
          is_success: false,
          error: error.message,
        };
      } else {
        error.message = getFrontErrorMessage(error.status);
        if (error.status === undefined) error.status = 500;
        return error;
      }
    }

    const data = {
      user: formData.get("user"),
      token: formData.get("token"),
      player: player_id,
      auth_data: auth_response,
    };
    const requestData = new HttpClientRequestData(
      "PATCH",
      `/tournament-validation/${id}`,
      data
    );

    requestData.headers["Content-Type"] = "default";
    const response = await this.handleResponse(requestData);
    return response;
  }

  async updateUserDetails(id, formData) {
    const data = {
      username: formData.get("username"),
      avatar: formData.get("avatar"),
    };
    const requestData = new HttpClientRequestData("PATCH", `/user/${id}`, data);
    requestData.headers["Content-Type"] = "application/x-www-form-urlencoded";
    const response = await this.handleResponse(requestData);
    return response;
  }
}

export default new GameService();
