import { AuthConstants } from '../constants/auth-constants.js';
import { HttpClient, HttpClientRequestData } from './httpClient.js';

class GameService {

  constructor() {
    this.baseUrl = 'http://localhost:8020';
    this.httpClient = new HttpClient(this.baseUrl);
  }

  async allGames() {
    const requestData = new HttpClientRequestData('GET', '/games');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async userGames() {
    const jwtToken = localStorage.getItem(AuthConstants.AUTH_TOKEN);
    console.log(jwtToken)
    const requestData = new HttpClientRequestData('GET', '/games');
    // const requestData = new HttpClientRequestData('GET', '/user/<uuid:pk>/games');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async getFormGame() {
    const requestData = new HttpClientRequestData('GET', '/game');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async addGame() {
    data = {}
    const requestData = new HttpClientRequestData('POST', '/game');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async game(id) {
    const requestData = new HttpClientRequestData('GET', `game/${id}`, data);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async updateGame(id) {
    data = {}
    const requestData = new HttpClientRequestData('PATCH', `game/${id}`, data);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async deleteGame(id) {
    const requestData = new HttpClientRequestData('DELETE', `game/${id}`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  // async login(formData) {
  //   const data = {
  //     email: formData.get('email'),
  //     password: formData.get('password'),
  //   };
  //   const requestData = new HttpClientRequestData('POST', 'sign-in/', data);
  //   const response = await this.httpClient.makeRequest(requestData);
  //   return response;
  // }

  // async validateTwoFactorCode(formData) {
  //   const data = {
  //     email: formData.get('email'),
  //     two_factor_code: formData.get('two-factor-code')
  //   };
  //   const requestData = new HttpClientRequestData('PUT', 'validate-2factor-code/', data);
  //   const response = await this.httpClient.makeRequest(requestData);
  //   return response;
  // }

}

export default new GameService();
