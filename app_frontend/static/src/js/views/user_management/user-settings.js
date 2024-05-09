import UserManagementView from './baseUserManagementView.js';
import { UserInformationService } from '../../services/userManagementService.js';

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
<div class="settings-container">
<div class="settings-form">
    <div class="avatar">
        <!-- User avatar image -->
        <img src="" alt="User Avatar">
        <button class="change-avatar">Change picture</button>
        <input type="file" id="avatar-input" accept="image/*" style="display: none;" />
    </div>
    <form id="user-settings-form">
        <!-- Email -->
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        <!-- Name -->
        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>
        <!-- Nickname -->
        <div class="form-group">
            <label for="nickname">Nickname:</label>
            <input type="text" id="nickname" name="nickname" required>
        </div>
        <!-- Two Factor Authentication -->
        <div class="form-group">
            <label for="two-factor-enabled">Two Factor Authentication:</label>
            <input type="checkbox" id="two-factor-enabled" name="two-factor-enabled">
        </div>
        <!-- Language Choice -->
        <div class="form-group">
            <label for="language">Language:</label>
            <select id="language" name="language">
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
            </select>
        </div>
        <button type="submit" class="btn-submit">Submit</button>
    </form>
</div>
</div>
`;

/**
 * Load the user data into the form fields.
 * @param {*} userInformationService - The user information service.
 * @returns {Promise<void>} - A promise that resolves when the user data is
 *  loaded.
 */
const loadUserData = async (userInformationService) => {
    var userData = await userInformationService.getUserData();
    userData = userData.user;

    const email = document.getElementById('email');
    const name = document.getElementById('name');
    const nickname = document.getElementById('nickname');
    const twoFactorEnabled = document.getElementById('two-factor-enabled');
    const avatar = document.querySelector('.avatar img');
    const language = document.getElementById('language');

    email.value = userData.email;
    name.value = userData.name;
    nickname.value = userData.nickname;
    twoFactorEnabled.checked = userData.two_factor_enabled;
    avatar.src = `http://localhost:3000/static/src/img/lili.jpg`;
    language.value = userData.chosen_language;
}

/**
 * Update the user data.
 * @param {*} userInformationService - The user information service.
 * @param {*} formData - The form data.
 * @returns {Promise<void>} - A promise that resolves when the user data is
 * updated.
 */
const updateUserData = async (userInformationService, formData) => {
    await userInformationService.updateUserData(formData);
}

const initFormSubmission = (userInformationService) => {
    const form = document.getElementById('user-settings-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);
        formData.append('avatar', document.getElementById('avatar-input').files[0]);
        await updateUserData(userInformationService, formData);
    });
};

const initAvatarChange = () => {
    console.log('initAvatarChange');
    const avatarButton = document.querySelector('.change-avatar');
    const avatarInput = document.getElementById('avatar-input');

    avatarButton.addEventListener('click', () => {
        avatarInput.click();
    });

    avatarInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const avatarImage = document.querySelector('.avatar img');
                avatarImage.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
};


/**
 * The action to run when the view is started.
 */
const action = async () => {
    const userId = '173b8552-8153-44b4-afe1-d7ce98235f77';
    const userInformationService = new UserInformationService(userId);

    await loadUserData(userInformationService);
    initAvatarChange();  // Initialize avatar change functionality
    initFormSubmission(userInformationService);  // Initialize form submission handling
};

export default new UserProfileView({ html, start: action });
