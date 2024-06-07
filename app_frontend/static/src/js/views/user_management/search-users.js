import { BlockingService, FriendshipRequestService, SearchUsersService } from '../../services/userManagementService.js';
import UserManagementView from './baseUserManagementView.js';

class searchUsersView extends UserManagementView {
  constructor(html, start) {
    super(html, start);
  }
}

/**
 * The HTML for the user profile view.
 * @type {string}
 */
const html = /*html*/`
<div class="row justify-content-center text-center mt-5">
  <div class="col-md-8">
    <h2 data-i18n-key="search--search-users">Search Users</h2>
    <div class="search-bar mb-4">
      <input type="text" id="searchInput" class="form-control">
      <button id="searchButton" class="btn btn-primary mt-2" data-i18n-key="search--title">Search</button>
    </div>
  </div>
</div>
<div class="row justify-content-center mt-4 hidden" id="searchResultsContainer">
  <div class="col-md-8">
    <div class="card">
      <div class="card-header">
        <h3 data-i18n-key="search--search-results">Search Results</h3>
      </div>
      <div class="card-body">
        <div id="searchResults" class="list-group"></div>
      </div>
    </div>
  </div>
</div>
<div class="row justify-content-center mt-5">
  <div class="col-md-8">
    <div class="card">
      <div class="card-header">
        <h3 data-i18n-key="search--currently-online">Currently Online Users</h3>
      </div>
      <div class="card-body">
        <div id="activeUsers" class="list-group"></div>
      </div>
    </div>
  </div>
</div>
`;

const start = async () => {

  const userId = 'af7aa1aa-d877-484d-b2a9-3d392531b8ab';

  const searchButton = document.getElementById('searchButton');
  const searchInput = document.getElementById('searchInput');
  const searchResultsContainer = document.getElementById('searchResultsContainer');
  const searchResults = document.getElementById('searchResults');
  const activeUsers = document.getElementById('activeUsers');

  const searchUsersService = new SearchUsersService();
  const friendshipRequestService = new FriendshipRequestService(userId);
  const blockingService = new BlockingService(userId);

  const isBlocked = async (user) => {
    const blockedUsers = await blockingService.getBlockedUsers();
    const blockedUsersIds = blockedUsers.blocked_users;
    return blockedUsersIds.some(blockedUserId => blockedUserId.id === user.id);
  };

  const filterBlockedUsers = async (users) => {
    const filteredUsers = [];
    for (const user of users) {
      if (!(await isBlocked(user))) {
        filteredUsers.push(user);
      }
    }
    return filteredUsers;
  };

  const performSearch = async () => {
    const query = searchInput.value;
    const response = await searchUsersService.searchUsers(query);
    const filteredUsers = await filterBlockedUsers(response.users);
    displaySearchResults(filteredUsers);
  };

  searchButton.addEventListener('click', performSearch);

  searchInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      performSearch();
    }
  });

  const displaySearchResults = (users) => {
    if (users.length > 0) {
      searchResultsContainer.classList.remove('hidden');
    } else {
      searchResultsContainer.classList.add('hidden');
    }
    searchResults.innerHTML = '';
    users.forEach(user => {
      const userItem = document.createElement('div');
      userItem.classList.add('list-group-item', 'd-flex', 'align-items-center', 'justify-content-between');
      const avatar = "https://localhost:8006" + user.avatar;
      userItem.innerHTML = `
                <div class="d-flex align-items-center">
                    <img src="${avatar}" alt="Avatar" class="rounded-circle" width="80" height="80">
                    <div class="ms-3">
                        <h5>${user.name} (@${user.nickname})</h5>
                    </div>
                </div>
                <div>
                    <button class="btn btn-primary btn-sm me-2" onclick="addFriend('${user.id}', this)">
                      <i class="bi bi-person-plus"></i>
                    </button>
                    <button class="btn btn-danger btn-sm me-2" onclick="blockUser('${user.id}', this)">
                      <i class="bi bi-person-x"></i>
                    </button>
                    <button class="btn btn-info btn-sm me-2" onclick="viewUserStats('${user.id}')">
                      <i class="bi bi-bar-chart"></i>
                    </button>
                </div>
            `;
      searchResults.appendChild(userItem);
    });
  };

  window.addFriend = async function (friendId, button) {
    const response = await friendshipRequestService.sendFriendRequest(friendId);
    alert(response.message);
    button.innerHTML = '<i class="bi bi-person-check"></i>';
  };

  window.blockUser = async function (blockId, button) {
    const response = await blockingService.blockUser(blockId);
    alert(response.message);
    button.closest('.list-group-item').remove();
  };

  const fetchActiveUsers = async () => {
    const response = await searchUsersService.viewOnlineUsers();
    if (response.users.length === 0) {
      activeUsers.innerHTML = '<p data-i18n-key="search--no-currently-online">There are no active users at the moment :(</p>';
      return;
    }
    displayActiveUsers(response.users);
  };

  const displayActiveUsers = (users) => {
    activeUsers.innerHTML = '';
    users.forEach(user => {
      const userItem = document.createElement('div');
      userItem.classList.add('list-group-item', 'd-flex', 'align-items-center', 'justify-content-between');
      userItem.innerHTML = `
                <div class="d-flex align-items-center">
                    <img src="${user.avatar}" alt="Avatar" class="rounded-circle" width="80" height="80">
                    <div class="ms-3">
                        <h5>${user.name} (@${user.nickname})</h5>
                    </div>
                </div>
            `;
      activeUsers.appendChild(userItem);
    });
  };

  fetchActiveUsers();
};

export default new searchUsersView({ html, start });
