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
  constructor(userId) {
    this.httpClient =
      new HttpClient(`http://localhost:8006/user/${userId}/`);
  }

  async getFriends() {
    const requestData = new HttpClientRequestData('GET', 'friends/');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async deleteFriend(friendId) {
    const requestData =
      new HttpClientRequestData('DELETE', `friends/${friendId}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }
}

/**
 * A service for managing blocked users.
 * @class
 */
class BlockingService {
  constructor(userId) {
    this.httpClient = new HttpClient(`http://localhost:8006/en/user/${userId}/`);
  }

  async getBlockedUsers() {
    const requestData = new HttpClientRequestData('GET', 'block/');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async blockUser(blockedUserId) {
    const requestData = new HttpClientRequestData('POST', `block/${blockedUserId}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async unblockUser(blockedUserId) {
    const requestData = new HttpClientRequestData('DELETE', `block/${blockedUserId}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }
}

/**
 * A service for managing friendship requests.
 * @class
 */
class FriendshipRequestService {
  constructor(userId) {
    this.httpClient = new HttpClient(`http://localhost:8006/en/user/${userId}/`);
  }

  async getFriendRequests() {
    const requestData = new HttpClientRequestData('GET', 'friend_request/');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async acceptFriendRequest(request_id) {
    const requestData = new HttpClientRequestData('PUT', `friend_request/${request_id}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async rejectFriendRequest(requestId) {
    const requestData = new HttpClientRequestData('DELETE', `friend_request/${requestId}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async sendFriendRequest(friendId) {
    const requestData = new HttpClientRequestData('POST', `friend_request/${friendId}/`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

}

/**
 * A service for managing user information.
 * @class
 */
class UserInformationService {

  constructor(userId) {
    this.httpClient = new HttpClient(`http://localhost:8006/user/${userId}`);

  }

  async getUserData() {
    const requestData = new HttpClientRequestData('GET', '/');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async updateUserData(formData) {
    const data = {
      email: formData.get('email'),
      name: formData.get('name'),
      nickname: formData.get('nickname'),
      two_factor_enabled: formData.get('two-factor-enabled') === 'on' ? true : false,
      avatar: formData.get('avatar'),
      chosen_language: formData.get('language'),
      avatar_name: formData.get('avatar').name
    };

    const requestData = new HttpClientRequestData('PATCH', '/', data);
    const response = await this.httpClient.makeRequest(requestData);

    return response;
  }

  async deleteUser() {
    const requestData = new HttpClientRequestData('DELETE', '/');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }
}
class SearchUsersService {

  constructor() {
    this.httpClient = new HttpClient('http://localhost:8006/user/');
  }

  async searchUsers(query) {
    const requestData = new HttpClientRequestData('GET', `?nickname=${query}`);
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }

  async viewOnlineUsers() {
    const requestData = new HttpClientRequestData('GET', '?status=active');
    const response = await this.httpClient.makeRequest(requestData);
    return response;
  }
}


export {
  BlockingService,
  FriendshipRequestService, FriendshipService, SearchUsersService, UserInformationService
};

