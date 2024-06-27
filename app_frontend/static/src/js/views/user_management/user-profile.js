import {
  BlockingService,
  FriendshipRequestService,
  FriendshipService,
  UserInformationService
} from '../../services/userManagementService.js';
import UserManagementView from '../baseLoggedView.js';
import languageHandler from '../../locale/languageHandler.js';

class UserProfileView extends UserManagementView {
  constructor(html, start) {
    super(html, start);
  }
}

/**
 * The HTML for the user profile view.
 * @type {string}
 */
const html = /*html*/`
<div class="container-fluid static-list scroll-on">
  <div class="row justify-content-center text-center">
    <div class="col-md-8">
      <div class="avatar">
        <img src="" alt="Avatar" class="img-fluid rounded-circle border border-warning mb-4">
      </div>
      <h2 id="userNickname"></h2>
      <h2 id="userStatus"></h2>
      <p id="user2fa"></p>
      <div class="lists-container d-flex flex-column align-items-center mt-4">
        <div class="friends-list col mb-4">
          <h3 data-i18n-key="profile--friends">Friends</h3>
          <p id="noFriendsMessage" hidden data-i18n-key="profile--no-friends">You have not added any friends yet :(</p>
          <ul id="friendsList" class="list-unstyled"></ul>
          <h4 data-i18n-key="profile--friend-requests">Friend Requests</h4>
          <p id="noFriendRequestsMessage" hidden data-i18n-key="profile--no-friend-requests">You have no friend requests</p>
          <ul id="friendRequests" class="list-unstyled"></ul>
        </div>
        <div class="blocked-list col">
          <h3 data-i18n-key="profile--blocked-users">Blocked Users</h3>
          <p id="noBlockedUsersMessage" hidden data-i18n-key="profile--no-blocked-users">You have not blocked any users yet</p>
          <ul id="blockedList" class="list-unstyled"></ul>
        </div>
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

  const userInformationService = new UserInformationService();
  const friendshipService = new FriendshipService();
  const blockingService = new BlockingService();
  const friendshipRequestService = new FriendshipRequestService();

  await loadUserData(userInformationService);
  await loadFriendsList(friendshipService);
  await loadBlockedUsers(blockingService);
  await loadFriendRequests(friendshipRequestService);
  initializeTooltips();
};

const initializeTooltips = () => {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.forEach((tooltip) => {
    const key = tooltip.getAttribute('data-i18n-tooltip');
    tooltip.setAttribute('title', languageHandler.translate(key));
  })
  const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

/**
 * Load the user data into the form fields.
 * @param {*} userInformationService - The user information service.
 * @returns {Promise<void>} - A promise that resolves when the user data is loaded.
 */
async function loadUserData(userInformationService) {
  const userDataResponse = await userInformationService.getUserData();
  const user = userDataResponse.user;

  const avatar = document.querySelector('.avatar img');
  avatar.src = `https://localhost:8006${user.avatar}`;
  document.getElementById('userNickname').innerText = `@${user.nickname.toLowerCase()}`;
  document.getElementById('userStatus').setAttribute('data-i18n-key', user.status == 'active' ? 'profile--active' : 'profile--inactive');
  document.getElementById('userStatus').innerText = user.status == 'active' ? 'Status: Online' : 'Status: Offline';
  document.getElementById('userStatus').classList.add(`status-${user.status}`);

  const user2fa = document.getElementById('user2fa');
  user2fa.setAttribute('data-i18n-key', user.two_factor_enabled ? 'profile--2fa-enabled' : 'profile--2fa-disabled');
  user2fa.innerHTML = user.two_factor_enabled 
    ? '<i class="bi bi-check-circle-fill" style="color: green;"></i> Two Factor Authentication'
    : '<i class="bi bi-x-circle-fill" style="color: red;"></i> Two Factor Authentication';
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

 const friendsList = document.getElementById('friendsList');
 const noFriendsMessage = document.getElementById('noFriendsMessage');

 if (friends.length === 0) {
   noFriendsMessage.hidden = false;
 } else {
   noFriendsMessage.hidden = true;
   document.querySelector('.friends-list').style.display = 'block';
   friends.forEach(friend => {
     const li = document.createElement('li');
     li.classList.add('d-flex', 'justify-content-between', 'align-items-center');
     li.innerText = friend.name;

     const unfriendBtn = document.createElement('button');
     unfriendBtn.innerHTML = '<i class="bi bi-person-dash-fill"></i>';
     unfriendBtn.classList.add('btn', 'btn-danger', 'btn-sm', 'ml-2');
     unfriendBtn.setAttribute('data-bs-toggle', 'tooltip');
     unfriendBtn.setAttribute('title', 'Unfriend User');
     unfriendBtn.setAttribute('data-i18n-key', 'profile--unfriend');
     unfriendBtn.setAttribute('data-i18n-tooltip', 'profile--unfriend');
     unfriendBtn.addEventListener('click', function () {
       unfriendUser(friend.user_uuid);
     });

     li.appendChild(unfriendBtn);
     friendsList.appendChild(li);
   });
   initializeTooltips();
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

 const blockedList = document.getElementById('blockedList');
 const noBlockedUsersMessage = document.getElementById('noBlockedUsersMessage');

 if (blockedUsers.length === 0) {
   noBlockedUsersMessage.hidden = false;
 } else {
   noBlockedUsersMessage.hidden = true;
   document.querySelector('.blocked-list').style.display = 'block';
   blockedUsers.forEach(blockedUser => {
     const li = document.createElement('li');
     li.classList.add('d-flex', 'justify-content-between', 'align-items-center');
     li.innerText = blockedUser.name;

     const unblockBtn = document.createElement('button');
     unblockBtn.innerHTML = '<i class="bi bi-unlock-fill"></i>';
     unblockBtn.classList.add('btn', 'btn-success', 'btn-sm', 'ml-2');
     unblockBtn.setAttribute('data-bs-toggle', 'tooltip');
     unblockBtn.setAttribute('title', 'Unblock User');
     unblockBtn.setAttribute('data-i18n-tooltip', 'profile--unblock');
     unblockBtn.setAttribute('data-i18n-key', 'profile--unblock');
     unblockBtn.addEventListener('click', function () {
       unblockUser(blockedUser.user_uuid);
     });

     li.appendChild(unblockBtn);
     blockedList.appendChild(li);
   });
   initializeTooltips();
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
 const activeFriendRequests = friendRequests.filter(request => request.is_active == true);

 const friendRequestsList = document.getElementById('friendRequests');
 const noFriendRequestsMessage = document.getElementById('noFriendRequestsMessage');

 if (friendRequests.length === 0 || activeFriendRequests.length === 0) {
   noFriendRequestsMessage.hidden = false;
 } else {
   noFriendRequestsMessage.hidden = true;
   document.querySelector('.friends-list').style.display = 'block';
   activeFriendRequests.forEach(request => {
     const li = document.createElement('li');
     li.classList.add('d-flex', 'justify-content-between', 'align-items-center');
     li.innerText = request.sender_name;

     const buttonsContainer = document.createElement('div');
     buttonsContainer.classList.add('friend-request-buttons', 'ml-2');

     const acceptBtn = document.createElement('button');
     acceptBtn.innerHTML = '<i class="bi bi-check-lg"></i>';
     acceptBtn.classList.add('btn', 'btn-success', 'btn-sm');
     acceptBtn.setAttribute('data-bs-toggle', 'tooltip');
     acceptBtn.setAttribute('title', 'Accept Friend Request');
     acceptBtn.setAttribute('data-i18n-key', 'profile--accept');
     acceptBtn.setAttribute('data-i18n-tooltip', 'profile--accept');
     acceptBtn.addEventListener('click', function () {
       acceptFriendRequest(request.id);
     });

     const rejectBtn = document.createElement('button');
     rejectBtn.innerHTML = '<i class="bi bi-x-lg"></i>';
     rejectBtn.classList.add('btn', 'btn-danger', 'btn-sm', 'ml-2');
     rejectBtn.setAttribute('data-bs-toggle', 'tooltip');
     rejectBtn.setAttribute('title', 'Reject Friend Request');
     rejectBtn.setAttribute('data-i18n-key', 'profile--reject');
     rejectBtn.addEventListener('click', function () {
       rejectFriendRequest(request.id);
     });

     buttonsContainer.appendChild(acceptBtn);
     buttonsContainer.appendChild(rejectBtn);
     li.appendChild(buttonsContainer);
     friendRequestsList.appendChild(li);
   });
   initializeTooltips();
 }
}


/**
 * Accept a friend request.
 * @param {string} requestId - The ID of the friend request.
 * @returns {Promise<void>} - A promise that resolves when the friend request
 * is accepted.
 */
async function acceptFriendRequest(requestId) {
  const friendshipRequestService = new FriendshipRequestService();
  await friendshipRequestService.acceptFriendRequest(requestId);
}

/**
 * Reject a friend request.
 * @param {string} requestId - The ID of the friend request.
 * @returns {Promise<void>} - A promise that resolves when the friend request
 * is rejected.
 */
async function rejectFriendRequest(requestId) {
  const friendshipRequestService = new FriendshipRequestService();
  await friendshipRequestService.rejectFriendRequest(requestId);
}

/**
 * Unfriend a user.
 * @param {string} friendId - The ID of the friend.
 * @returns {Promise<void>} - A promise that resolves when the user is unfriended.
 */
async function unfriendUser(friendId) {
  const friendshipService = new FriendshipService();
  await friendshipService.deleteFriend(friendId);
}

/**
 * Unblock a user.
 * @param {string} blockedUserId - The ID of the blocked user.
 * @returns {Promise<void>} - A promise that resolves when the user is unblocked.
 */
async function unblockUser(blockedUserId) {
  const blockingService = new BlockingService();
  await blockingService.unblockUser(blockedUserId);
}

export default new UserProfileView({ html, start });
