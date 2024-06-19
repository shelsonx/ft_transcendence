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

const userLabel = "My games"
const allUsersLabel = "All games"

const html = /*html*/`
  <div class="d-flex justify-content-between">
    <h2 id="hello-user"></h2>
    <div>
      <button id="btn-data-switch" type="button" class="btn btn-info">
        ${userLabel}
      </button>
      <button id="btn-play" type="button" class="btn btn-primary"
        onclick="window.location='#play';"
      >
        Play
      </button>
    </div>
  </div>
  <div class="container-fluid main scroll-on mt-3">
    <div id="home-container" class="static-list"></div>
  </div>
`

const swap = (response) => {
  // TODO: lidar quando retornar erro ou não responder
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

  let userData = false
  const btnDataSwitch = document.getElementById("btn-data-switch");
  btnDataSwitch.addEventListener("click", async () => {
    userData = !userData

    if (userData) {
      await gameService.userGames(user.id).then(swap);
      btnDataSwitch.innerHTML = allUsersLabel;
      }
    else {
      await gameService.allGames().then(swap);
      btnDataSwitch.innerHTML = userLabel;
    }
  });

}

export default new HomeView(html, start);
