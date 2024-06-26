import { UserInformationService } from '../../services/userManagementService.js';
import languageHandler from "../../locale/languageHandler.js";

import { getUserId } from '../../utils/getUserId.js';
import UserManagementView from '../baseLoggedView.js';
import gameService from '../../services/gameService.js';
import wrapperLoadingService from "../../services/wrapperService.js";
import authService from "../../services/authService.js";
import gameInfoService from '../../services/gameInfoService.js';

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
        <img src="" alt="Avatar">
        <button class="change-avatar" data-i18n-key="settings--change-picture">Change Picture</button>
        <input type="file" id="avatar-input" accept="image/*" style="display: none;" />
    </div>
    <form id="user-settings-form">
        <!-- Name -->
        <div class="form-group">
            <label for="name" data-i18n-key="settings--name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>
        <!-- Nickname -->
        <div class="form-group">
            <label for="nickname" data-i18n-key="settings--nickname">Nickname:</label>
            <input type="text" id="nickname" name="nickname" required>
        </div>
        <!-- Two Factor Authentication -->
        <div class="form-group">
            <label for="two-factor-enabled" data-i18n-key="settings--Two-Factor-Authentication">Two Factor Authentication:</label>
            <input type="checkbox" id="two-factor-enabled" name="two-factor-enabled">
        </div>
        <!-- Language Choice -->
        <div class="form-group">
            <label for="language" data-i18n-key="settings--language">Language:</label>
            <select id="language" name="language">
                <option value="en" data-i18n-key="settings--english">English</option>
                <option value="pt-br" data-i18n-key="settings--portuguese">Portuguese</option>
                <option value="fr" data-i18n-key="settings--french">French</option>
            </select>
        </div>
        <button type="submit" class="btn-submit" data-i18n-key="settings--submit">Submit</button>
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

    const name = document.getElementById('name');
    const nickname = document.getElementById('nickname');
    const twoFactorEnabled = document.getElementById('two-factor-enabled');
    const avatar = document.querySelector('.avatar img');
    const language = document.getElementById('language');

    name.value = userData.name;
    nickname.value = userData.nickname;
    twoFactorEnabled.checked = userData.two_factor_enabled;
    avatar.src = `https://localhost:8006${userData.avatar}`;
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
    return await wrapperLoadingService.execute(
      userInformationService,
      userInformationService.updateUserData,
      formData
    );
}

const changeLanguage = (selectedLanguage) => {
  if (selectedLanguage) {
    languageHandler.setDefaultLocale(selectedLanguage);
    languageHandler.changeLanguage(selectedLanguage);
  }
}

const rollBackChanges = async (user) => {
  await authService.updateUserData(user.id, {
    user_name: user.name,
    enable_2fa: user.enable_2fa,
  });
};

const initFormSubmission = (userInformationService, user) => {
  const userId = getUserId();
  const form = document.getElementById('user-settings-form');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const avatarInput = document.getElementById('avatar-input');
    const avatarFile = avatarInput.files[0];

    if (avatarFile) {
      const extension = avatarFile.name.split('.').pop();
      const uniqueIdentifier = `${userId}_${Date.now()}.${extension}`;
      formData.append('avatar', avatarFile);
      formData.append('avatar_name', uniqueIdentifier);
    }

    const authData = {
      user_name: formData.get("nickname"),
      enable_2fa: !!formData.get("two-factor-enabled"),
    };

    const response = await wrapperLoadingService.execute(
      authService,
      authService.updateUserData,
      user.id,
      authData
    );

    if (!response.is_success) return;

    const userData = await userInformationService.getUserData();
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
    const userDataResponse = await updateUserData(userInformationService, data);
    if (!userDataResponse.is_success) return await rollBackChanges(user);

    const gameDataResponse = await gameService.updateUserDetails(user.id, formData);
    if (!gameDataResponse.is_success) return await rollBackChanges(user);

    const gameInfoResponse = await gameInfoService.updateUserInformation({
      id_msc: userId,
      nickname: formData.get("nickname"),
      avatar: `/media/avatars/${formData.get("avatar_name")}`,
    });

    if (gameInfoResponse !== "OK") return await rollBackChanges(user);

    changeLanguage(formData.get("language"));
  });
};

const initAvatarChange = () => {
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
const action = async (user) => {
    const userInformationService = new UserInformationService();

    await loadUserData(userInformationService);
    initAvatarChange();
    initFormSubmission(userInformationService, user);
  };

export default new UserProfileView({ html, start: action });
