import { AuthConstants } from '../constants/auth-constants.js';
import { HttpClientRequestData } from './httpClient.js';
import { LanguageService } from './languageService.js';

class AuthService extends LanguageService {

  constructor() {
    super('https://localhost:8010/api/auth/');
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

  /**
   * Asynchronously updates user data.
   *
   * This function sends a PUT request to update user data such as username, password, and two-factor authentication status.
   * It constructs a request with the provided data and sends it using the `makeRequest` method.
   *
   * @param {Object} data - The data to update for the user.
   * @param {string} data.user_name - The new username of the user.
   * @param {string} data.password - The new password of the user.
   * @param {string} data.old_password - The old password of the user, required for authentication.
   * @param {boolean} data.enable_2fa - Indicates whether two-factor authentication should be enabled or disabled.
   *
   * @returns {Promise<Object>} The response from the server after attempting to update the user data. The response object includes:
   * - `data`: An object containing the updated user data, including `id`, `user_name`, `email`, `login_type`, `enable_2fa`, `created_at`, `updated_at`, and `is_active` fields.
   * - `message`: A string indicating the result of the request.
   * - `is_success`: A boolean indicating whether the update was successful.
   */
  async updateUserData(userId, data) {
    const requestData = new HttpClientRequestData('PUT', `user/${userId}/`, data);
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

  async sendGame2Factor(data) {
    const requestData = new HttpClientRequestData('POST', 'game-2factor-code/', data);
    const response = await this.makeRequest(requestData);
    return response;
  }

  async validateGame2Factor(data) {
    const requestData = new HttpClientRequestData('PUT', 'game-2factor-code/', data);
    const response = await this.makeRequest(requestData);
    return response;
  }

  logout() {
    localStorage.removeItem(AuthConstants.AUTH_TOKEN);
    window.location.href = '/#login';
  }

}

export default new AuthService();
