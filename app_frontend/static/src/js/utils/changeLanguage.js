import { AuthConstants } from '../constants/auth-constants.js';
import languageHandler from '../locale/languageHandler.js';
import {
  UserInformationService
} from '../services/userManagementService.js';

export const changeLanguageWhenLogin = async (userId) => {
  try {
    const userInfoService = new UserInformationService(userId);
    const { user: userManagement } = await userInfoService.getUserData();
    const { chosen_language } = userManagement;
    const userChoosenLanguage = chosen_language || localStorage.getItem(AuthConstants.AUTH_LOCALE);
    languageHandler.setDefaultLocale(userChoosenLanguage);
    languageHandler.changeLanguage(userChoosenLanguage);
  } catch (err) {
    console.error(err);
  }
};
