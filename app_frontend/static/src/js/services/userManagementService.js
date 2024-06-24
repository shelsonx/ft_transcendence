import { getUserId } from '../utils/getUserId.js';
import { HttpClient, HttpClientRequestData } from './httpClient.js';

/**
 * All the services related to user management.
 * @module userManagementService
 */

/**
 * A service for managing friendships.
 * @class
 */
class FriendshipService {
  constructor() {
    this.userId = getUserId();
    this.httpClient = new HttpClient(`https://localhost:8006`);
  }

  async getFriends() {
    const requestData = new HttpClientRequestData('GET', `/user/${this.userId}/friends/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async deleteFriend(friendId) {
    const requestData = new HttpClientRequestData('DELETE', `/user/${this.userId}/friends/${friendId}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }
}

/**
 * A service for managing blocked users.
 * @class
 */
class BlockingService {
  constructor() {
    this.userId = getUserId();
    this.httpClient = new HttpClient(`https://localhost:8006`);
  }

  async getBlockedUsers() {
    const requestData = new HttpClientRequestData('GET', `/user/${this.userId}/block/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async blockUser(blockedUserId) {
    const requestData = new HttpClientRequestData('POST', `/user/${this.userId}/block/${blockedUserId}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async unblockUser(blockedUserId) {
    const requestData = new HttpClientRequestData('DELETE', `/user/${this.userId}/block/${blockedUserId}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }
}

/**
 * A service for managing friendship requests.
 * @class
 */
class FriendshipRequestService {
  constructor() {
    this.userId = getUserId();
    this.httpClient = new HttpClient(`https://localhost:8006`);
  }

  async getFriendRequests() {
    const requestData = new HttpClientRequestData('GET', `/user/${this.userId}/friend_request/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async acceptFriendRequest(requestId) {
    const requestData = new HttpClientRequestData('PUT', `/user/${this.userId}/friend_request/${requestId}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async rejectFriendRequest(requestId) {
    const requestData = new HttpClientRequestData('DELETE', `/user/${this.userId}/friend_request/${requestId}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async sendFriendRequest(friendId) {
    const requestData = new HttpClientRequestData('POST', `/user/${this.userId}/friend_request/${friendId}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

}

/**
 * A service for managing user information.
 * @class
 */
class UserInformationService {
  constructor() {
    this.userId = getUserId();
    this.httpClient = new HttpClient(`https://localhost:8006`);

  }

  async getUserData() {
    const requestData = new HttpClientRequestData('GET', `/user/${this.userId}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async updateUserData(formData) {
    const userData = await this.getUserData();
    const email = userData.user.email;

    const data = {
      name: formData.get('name'),
      nickname: formData.get('nickname'),
      two_factor_enabled: formData.get('two-factor-enabled') === 'on' ? true : false,
      avatar: formData.get('avatar'),
      chosen_language: formData.get('language'),
      user_uuid: getUserId(),
      email: email,
      avatar_name: formData.get('avatar_name')
      };

    const requestData = new HttpClientRequestData('PATCH', `/user/${this.userId}/`, data);
    const response = await this.httpClient.makeRequest(requestData);

    return response;
  }

  async deleteUser() {
    const requestData = new HttpClientRequestData('DELETE', `/user/${this.userId}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }
}
class SearchUsersService {

  constructor() {
    this.httpClient = new HttpClient('https://localhost:8006');
  }

  async searchUsers(query) {
    const requestData = new HttpClientRequestData('GET', `/user/?nickname=${query}`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async viewOnlineUsers() {
    const requestData = new HttpClientRequestData('GET', '/user/?status=active');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }
}


export {
  BlockingService,
  FriendshipRequestService, FriendshipService, SearchUsersService, UserInformationService
};

