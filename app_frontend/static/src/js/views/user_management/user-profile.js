import UserManagementView from './baseUserManagementView.js';
import {
  FriendshipService,
  BlockingService,
  FriendshipRequestService,
  UserInformationService
} from '../../services/userManagementService.js';

class UserProfileView extends UserManagementView {
  constructor(html, start) {
    super(
      html,
      start
    );
  }
}

/**
 * The HTML for the user profile view.
 * @type {string}
 */
const html = /*html*/`
  <div class="row justify-content-center text-center">
    <div class="col-md-8">
      <div class="avatar">
        <img src="" alt="User Avatar">
      </div>
      <h2 id="userNickname"></h2>
      <h2 id="userStatus"></h2>
      <p id="userLanguage"></p>
      <p id="user2fa"></p>
      <div class="lists-container d-flex justify-content-between mt-4">
      <div class="friends-list col">
          <h3>Friends</h3>
          <ul id="friendsList" class="friends-list-unstyled">
          </ul>
          <h4>Friend Requests</h4>
          <ul id="friendRequests" class="friends-list-unstyled">
          </ul>
        </div>
        <div class="blocked-list col">
          <h3>Blocked Users</h3>
          <ul id="blockedList" class="blocked-list-unstyled">
          </ul>
        </div>
      </div>
    </div>
  </div>
`;

/**
 * Start the user profile view.
 * @returns {Promise<void>} - A promise that resolves when the view is started.
 */
const start = async () => {
  const userId = '97e30085-8d7a-49b9-8a98-aabf2dfe3105';

  const userInformationService = new UserInformationService(userId);
  const friendshipService = new FriendshipService(userId);
  const blockingService = new BlockingService(userId);
  const friendshipRequestService = new FriendshipRequestService(userId);

  await loadUserData(userInformationService);
  await loadFriendsList(friendshipService);
  await loadBlockedUsers(blockingService);
  await loadFriendRequests(friendshipRequestService);
};

/**
 * Load the user data into the form fields.
 * @param {*} userInformationService - The user information service.
 * @returns {Promise<void>} - A promise that resolves when the user data is
 * loaded.
 */
async function loadUserData(userInformationService) {
  const userDataResponse = await userInformationService.getUserData();
  const user = userDataResponse.user;

  const avatar = document.querySelector('.avatar img');
  avatar.src = `http://localhost:8000${user.avatar}`
  console.log(avatar.src);
  document.getElementById('userNickname').innerText = `@${user.nickname}`
  document.getElementById('userStatus').innerText = user.status == 'active' ? 'Active' : 'Inactive';
  document.getElementById('userStatus').classList.add(`status-${user.status}`);
  document.getElementById('userLanguage').innerText = `Language: ${user.chosen_language.toUpperCase()}`
  document.getElementById('user2fa').innerText = user.twoFactorAuth ? '2FA: Enabled' : '2FA: Disabled';
}

/**
 * Load the friends list.
 * @param {*} friendshipService - The friendship service.
 * @returns {Promise<void>} - A promise that resolves when the friends list is
 * loaded.
 */
async function loadFriendsList(friendshipService) {
  const friendshipDataResponse = await friendshipService.getFriends();
  const friends = friendshipDataResponse.friends;

  if (friends.length == 0) {
    document.getElementById('friendsList').innerText = 'You have not added any friends yet :(';
  } else {
    document.querySelector('.friends-list').style.display = 'block';
    friends.forEach(friend => {
      const li = document.createElement('li');
      li.innerText = friend.name;
      friendsList.appendChild(li);
    });
  }
}

/**
 * Load the blocked users list.
 * @param {*} blockingService - The blocking service.
 * @returns {Promise<void>} - A promise that resolves when the blocked users
 * list is loaded.
 */
async function loadBlockedUsers(blockingService) {
  const blockDataResponse = await blockingService.getBlockedUsers();
  const blockedUsers = blockDataResponse.blocked_users;

  if (blockedUsers.length == 0) {
    document.getElementById('blockedList').innerText = 'You have not blocked any users yet';
  } else {
    document.querySelector('.blocked-list').style.display = 'block';
    blockedUsers.forEach(blockedUser => {
      const li = document.createElement('li');
      li.innerText = blockedUser;
      blockedList.appendChild(li);
    });
  }
}

/**
 * Load the friend requests.
 * @param {*} friendshipRequestService - The friendship request service.
 * @returns {Promise<void>} - A promise that resolves when the friend requests
 * are loaded.
 */
async function loadFriendRequests(friendshipRequestService) {
  const friendshipRequestDataResponse = await friendshipRequestService.getFriendRequests();
  const friendRequests = friendshipRequestDataResponse.friend_requests;

  if (friendRequests.length == 0) {
    document.getElementById('friendRequests').innerText = 'You have no friend requests';
  } else {
    document.querySelector('.friends-list').style.display = 'block';
    friendRequests.forEach(request => {
      const li = document.createElement('li');
      li.innerText = request.name;

      const acceptBtn = document.createElement('button');
      acceptBtn.innerText = 'Accept';
      acceptBtn.classList.add('btn', 'btn-success', 'btn-sm', 'ml-2');
      acceptBtn.addEventListener('click', function () {
        acceptFriendRequest(request.id);
      });

      li.appendChild(acceptBtn);
      friendRequests.appendChild(li);
    });
  }
}


/**
 * Accept a friend request.
 * @param {string} requestId - The ID of the friend request.
 * @returns {Promise<void>} - A promise that resolves when the friend request
 * is accepted.
 */
async function acceptFriendRequest(requestId) {
  console.log('Accepting friend request with ID:', requestId);
}

export default new UserProfileView({ html, start });
