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
  <div class="d-flex justify-content-between">
    <h2 id="hello-user"></h2>
    <div>
      <button id="btn-my-games" type="button" class="btn btn-info"
        onclick="window.location='#my-games';"
      >
        My games
      </button>
      <button id="btn-play" type="button" class="btn btn-primary"
        onclick="window.location='#play';"
      >
        Play
      </button>
    </div>
  </div>
  <div class="container-fluid main-game scroll-on mt-3">
    <div id="home-container" class="static-list"></div>
  </div>

  <div id="error-message" class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
  </div>
`

const loadErrorMessage = (error) => {
  const message = document.getElementById("error-message");
  message.innerHTML = /*html*/ `
    <h1 class="game-message text-center">${error.status} <br> ${error.message}</h1>`;
};

const swap = (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response);
    return;
  }

  const swapContainer = document.getElementById("home-container");
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

  await gameService.allGames().then(swap);
}

export default new HomeView(html, start);
