import { AuthConstants } from '../constants/auth-constants.js';
import languageHandler from '../locale/languageHandler.js';
import {
  UserInformationService
} from '../services/userManagementService.js';

export const changeLanguageWhenLogin = async (userId) => {
  let userChoosenLanguage = localStorage.getItem(AuthConstants.AUTH_LOCALE) || 'en';
  try {
    const userInfoService = new UserInformationService(userId);
    const { user: userManagement } = await userInfoService.getUserData();
    const { chosen_language } = userManagement;
    userChoosenLanguage = chosen_language;
    languageHandler.setDefaultLocale(userChoosenLanguage);
  } catch (err) {
    console.error(err);
  } finally {
    languageHandler.changeLanguage(userChoosenLanguage);
   }
};
