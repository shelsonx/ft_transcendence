import { AuthConstants } from '../constants/auth-constants.js';
import { HttpClientRequestData } from './httpClient.js';
import { LanguageService } from './languageService.js';

class AuthService extends LanguageService{

  constructor() {
    super('http://localhost:8002/api/auth/');
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
      window.location.href = '/#';
    } else {
      window.location.href = '?email=' + email + '#two-factor-auth';
    }
  }

  async login(formData) {
    const data = {
      email: formData.get('email'),
      password: formData.get('password'),
    };
    const requestData = new HttpClientRequestData('POST', 'sign-in/', data);
    const response = await this.makeRequest(requestData);
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
    const response = await this.makeRequest(requestData);
    return response;
  }

  async validateTwoFactorCode(formData) {
    const data = {
      email: formData.get('email'),
      two_factor_code: formData.get('two-factor-code')
    };
    const requestData = new HttpClientRequestData('PUT', 'validate-2factor-code/', data);
    const response = await this.makeRequest(requestData);
    return response;
  }

  async resendTwoFactorCode(email) {
    const data = {
      email,
    };
    const requestData = new HttpClientRequestData('POST', 'validate-2factor-code/', data);
    const response = await this.makeRequest(requestData);
    return response;
  }


  async getMe() {
    const requestData = new HttpClientRequestData('GET', 'user/');
    const response = await this.makeRequest(requestData);
    return response;
  }

  async login42() {
   window.location.assign(`${this.baseApi}redirect-42/`);
  }

  async register42() {
    const requestData = new HttpClientRequestData('GET', 'register-42/');
    const response = await this.makeRequest(requestData);
    return response;
  }

  async forgotPassword(formData) {
    const data = {
      email: formData.get('email'),
      two_factor_code: formData.get('two-factor-code'),
      password: formData.get('password'),
      confirm_password: formData.get('confirm-password')
    };
    const requestData = new HttpClientRequestData('POST', 'forgot-password/', data);
    const response = await this.makeRequest(requestData);
    return response;
  }

  logout() {
    localStorage.removeItem(AuthConstants.AUTH_TOKEN);
    window.location.href = '/#login';
  }

}

export default new AuthService();
