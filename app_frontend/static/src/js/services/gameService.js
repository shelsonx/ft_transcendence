import { AuthConstants } from "../constants/auth-constants.js";
import { getErrorMessage } from "../utils/errors.js";
import { HttpClient, HttpClientRequestData } from "./httpClient.js";

class GameService {
  constructor() {
    this.baseUrl = "https://localhost:8020";
    this.httpClient = new HttpClient(this.baseUrl);
  }

  async handleResponse(requestData) {
    try {
      const response = await this.httpClient.makeRequest(requestData);
      return response;
    } catch (error) {
      const message = getErrorMessage(error.status);
      if (message != undefined)
        error.message = message;
      // else
      //   error.message = getErrorMessage(500);
      //   error.status = 500;
      return error
    }
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
    console.log("Request", requestData);
    const response = await this.handleResponse(requestData);
    return response;
  }

  async game(id) {
    const requestData = new HttpClientRequestData("GET", `/game/${id}`);
    const response = await this.handleResponse(requestData);
    return response;
  }

  async updateGame(id, game) {
    const data = {
      game_datetime: game.game_datetime,
      status: game.status,
      duration: game.duration,
      player_left: game.player_left,
      player_right: game.player_right,
    };
    const requestData = new HttpClientRequestData("PATCH", `/game/${id}`, data);
    requestData.headers["Content-Type"] = "application/x-www-form-urlencoded";
    const response = await this.handleResponse(requestData);
    return response;
  }

  async validateGame(id) {
    const requestData = new HttpClientRequestData(
      "PATCH",
      `/game-validation/${id}`
    );
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

  async addTournament() {
    const data = {};
    const requestData = new HttpClientRequestData("POST", "/tournament", data);
    const response = await this.handleResponse(requestData);
    return response;
  }

  async tournament(id) {
    const requestData = new HttpClientRequestData("GET", `/tournament/${id}`);
    const response = await this.handleResponse(requestData);
    return response;
  }


  async deleteTournament(id) {
    const requestData = new HttpClientRequestData("DELETE", `/tournament/${id}`);
    const response = await this.handleResponse(requestData);
    return response;
  }
}

export default new GameService();
