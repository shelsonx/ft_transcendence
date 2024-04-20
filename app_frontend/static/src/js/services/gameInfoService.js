import { HttpClient, HttpClientRequestData } from './httpClient.js';

class GameInfoService {

  constructor() {
    this.httpClient = new HttpClient('http://localhost:8003/dash/');
  }
  async gameInfo(formData) {
    /* const data = {
      email: formData.get('email'),
      user_name: formData.get('username'),
      password: formData.get('password'),
      confirm_password: formData.get('confirm-password')
    }; */
    const requestData = new HttpClientRequestData('GET', 'home/');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }
}

export default new GameInfoService();