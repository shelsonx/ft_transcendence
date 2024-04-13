import { AuthConstants } from '../constants/auth-constants.js';
import { HttpClient, HttpClientRequestData } from './httpClient.js';

class AuthService {

  constructor() {
    this.httpClient = new HttpClient('http://localhost:8002/api/auth/');
  }

  addTokenToLocalStorage(response) {
    if (response.is_success) {
      localStorage.setItem(AuthConstants.AUTH_TOKEN, response.data.token);
    }
  }

  redirectIfAuthenticated(response, email) {
    if (typeof response?.data?.is_temporary_token === 'undefined') {
      return ;
    }
    if (response.data.is_temporary_token === false) {
       window.location.hash = '#';
    } else {
       window.location.hash = '#two-factor-auth?email=' + email;
    }
  }

  async login(formData) {
    const data = {
      email: formData.get('email'),
      password: formData.get('password'),
    };
    const requestData = new HttpClientRequestData('POST', 'sign-in/', data);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async register(formData) {
    const data = {
      email: formData.get('email'),
      user_name: formData.get('username'),
      password: formData.get('password'),
      confirm_password: formData.get('confirm-password')
    };
    const requestData = new HttpClientRequestData('POST', 'sign-up/', data);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

}

export default new AuthService();