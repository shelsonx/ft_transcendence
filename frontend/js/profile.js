console.log('Profile page script loaded');

document.addEventListener("DOMContentLoaded", () => {
    fetchUserProfile();
});

async function fetchUserProfile() {
    try {
        const response = await fetch('http://localhost:8000/user/e6751c59-ee23-4a25-8eba-60c4090b3511/', {
            method: 'GET',
        });
        const data = await response.json();
        const user = data.user;
        document.getElementsByClassName('avatar')[0].appendChild(new Image(100, 100)).src = user.avatar;
        document.getElementById('userName').textContent = user.name;
        document.getElementById('userNickname').textContent = "@" + user.nickname.toLowerCase();
        document.getElementById('userStatus').textContent = `Status: ${user.status.toUpperCase()}`;
        document.getElementById('userStatus').className = user.status.toLowerCase() === 'active' ? 'status-active' : 'status-inactive';
        document.getElementById('user2fa').textContent = `Two-Factor Authentication: ${user.two_factor_enabled ? 'Enabled' : 'Disabled'}`;
        document.getElementById('userLanguage').textContent = `Choosen Language: ${user.chosen_language.toUpperCase()}`;
        const friendsList = document.getElementById('friendsList');
        user.friends.forEach(friend => {
            const listItem = document.createElement('li');
            listItem.textContent = friend.name;
            friendsList.appendChild(listItem);
        });
        const blockedList = document.getElementById('blockedList');
        user.blocked_users.forEach(blockedUser => {
            const listItem = document.createElement('li');
            listItem.textContent = blockedUser.name;
            blockedList.appendChild(listItem);
        });
    } catch (error) {
        console.error('Error fetching user profile:', error);
    }
}

export { fetchUserProfile };
