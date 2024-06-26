import { AuthConstants } from '../constants/auth-constants.js';
import languageHandler from '../locale/languageHandler.js';
import gameService from '../services/gameService.js';
import {
  UserInformationService
} from '../services/userManagementService.js';
import { loadErrorMessage } from '../utils/errors.js';
import BaseLoggedView from './baseLoggedView.js';
import { CustomEvents } from "../constants/custom-events.js";

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
    <h3 class="px-3" class="d-inline-flex">
      <span class="h3" id="hello-user"></span><span class="h3" id="user-name"></span>
    </h3>
    <div>
      <button id="btn-my-games" type="button" class="btn btn-info"
        onclick="window.location='#my-games';" data-i18n-key="my-games-button"
      >
        My Games
      </button>
      <button id="btn-play" type="button" class="btn btn-primary"
        onclick="window.location='#play';" data-i18n-key="play-button"
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


const swap = (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "error-message");
    return;
  }

  const swapContainer = document.getElementById("home-container");
  swapContainer.innerHTML = response;
};


const start = async (user) => {
  if (user) {
    const helloUser = document.getElementById("hello-user");
    helloUser.setAttribute("data-i18n-key", "hello-user");
    helloUser.innerHTML = "Hello, ";
    const userName = document.getElementById("user-name");
    userName.innerHTML = `, ${user.userName}!`;

  }
  await gameService.allGames().then(swap);
  window.addEventListener(CustomEvents.LANGUAGE_CHANGE_EVENT, async (e) => {
    await gameService.allGames().then(swap);
  });
};

export default new HomeView(html, start);
