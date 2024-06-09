import languageHandler from '../locale/languageHandler.js';
import gameService from '../services/gameService.js';
import {
  UserInformationService
} from '../services/userManagementService.js';
import BaseLoggedView from './baseLoggedView.js';
class HomeView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start
    },
    );
  }
}

const html = /*html*/`
  <h2 id="hello-user"></h2>
  <div id="swap-container" class="container-fluid main"></div>
`

const swap = (response) => {
  // TODO: lidar quando retornar erro ou não responder
  const swapContainer = document.getElementById("swap-container");
  swapContainer.innerHTML = response;
}

const changeLanguageWhenLogin = async (userId) => {
  // TODO
  let userChoosenLanguage = 'en';
  try {
    const userInfoService = new UserInformationService(userId);
    const { user: userManagement } = await userInfoService.getUserData();
    const { chosen_language } = userManagement;
    userChoosenLanguage = chosen_language;
  } catch (err) {
    console.error(err);
  }
  languageHandler.changeLanguage(userChoosenLanguage);
}

const start = async (user) => {
  if (user) {
    changeLanguageWhenLogin(user.id);
  }
  const helloUser = document.getElementById("hello-user");
  helloUser.innerHTML = `Hello, ${user.userName}!`;
  await gameService.userGames().then(swap);
}

export default new HomeView(html, start);
