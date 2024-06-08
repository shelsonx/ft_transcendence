import { AuthConstants } from '../constants/auth-constants.js';
import { HttpClient, HttpClientRequestData } from './httpClient.js';

class GameService {

  constructor() {
    this.baseUrl = 'https://localhost:8020';
    this.httpClient = new HttpClient(this.baseUrl);
  }

  async allGames() {
    const requestData = new HttpClientRequestData('GET', '/games');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async userGames() {
    const requestData = new HttpClientRequestData('GET', '/games');
    // const requestData = new HttpClientRequestData('GET', '/user/<uuid:pk>/games');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async getFormGame() {
    const requestData = new HttpClientRequestData('GET', '/add-game');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async addGame(formData) {
    const jwtToken = localStorage.getItem(AuthConstants.AUTH_TOKEN);
    // console.log(jwtToken)
    const data = {
      points_to_win: formData.get("points_to_win"),
      username: formData.get("username"),
      csrfmiddlewaretoken: formData.get("csrfmiddlewaretoken"),
    }
    const requestData = new HttpClientRequestData('POST', '/add-game');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async game(id) {
    const requestData = new HttpClientRequestData('GET', `/game/${id}`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async updateGame(id) {
    const data = {}
    const requestData = new HttpClientRequestData('PATCH', `/game/${id}`, data);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async deleteGame(id) {
    const requestData = new HttpClientRequestData('DELETE', `/game/${id}`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async allTournaments() {
    const requestData = new HttpClientRequestData('GET', '/tournaments');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async userTournaments() {
    const jwtToken = localStorage.getItem(AuthConstants.AUTH_TOKEN);
    console.log(jwtToken)
    const requestData = new HttpClientRequestData('GET', '/tournaments');
    // const requestData = new HttpClientRequestData('GET', '/user/<uuid:pk>/tournaments');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async getFormTournament() {
    const requestData = new HttpClientRequestData('GET', '/tournament');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async addTournament() {
    const data = {}
    const requestData = new HttpClientRequestData('POST', '/tournament');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async tournament(id) {
    const requestData = new HttpClientRequestData('GET', `tournament/${id}`, data);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async updateTournament(id) {
    const data = {}
    const requestData = new HttpClientRequestData('PATCH', `tournament/${id}`, data);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async deleteTournament(id) {
    const requestData = new HttpClientRequestData('DELETE', `tournament/${id}`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

}

export default new GameService();
