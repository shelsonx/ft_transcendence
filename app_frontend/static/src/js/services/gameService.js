import { AuthConstants } from '../constants/auth-constants.js';
import { HttpClient, HttpClientRequestData } from './httpClient.js';

class GameService {

  constructor() {
    this.baseUrl = 'http://localhost:8020';
    this.httpClient = new HttpClient(this.baseUrl);
  }

  async gameTest() {
    const requestData = new HttpClientRequestData('GET', '/');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async allGames() {
    const requestData = new HttpClientRequestData('GET', '/games');
    // const requestData = new HttpClientRequestData('GET', '/games/8cd4dcd1-3055-459a-8c67-b7bdc7194b85');
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
