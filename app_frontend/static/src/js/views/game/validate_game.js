import BaseLoggedView from "../baseLoggedView.js";
import gameService from "../../services/gameService.js";
import { loadErrorMessage, pageNotFoundMessage } from "../../utils/errors.js";
import { VerificationType } from "../../contracts/game/validation.js";
import authService from "../../services/authService.js";
import wrapperLoadingService from '../../services/wrapperService.js';

class ValidateGameView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div class="main-game scroll-on container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
    <div id="verify-game-container" class="static"></div>
  </div>
`;

let match = null;

const putVerifyForm = async (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "verify-game-container");
    return;
  }

  const swapContainer = document.getElementById("verify-game-container");
  swapContainer.innerHTML = response;

  const verifyForm = document.getElementById("validation-form");
  verifyForm.addEventListener("submit", submitVerifyForm);

  const resendCodeButton = document.getElementById("resend-btn");
  resendCodeButton.addEventListener("click", resendCode)
};

const resendCode = (e) => {
  const verifyForm = document.getElementById("validation-form");
  const formData = new FormData(verifyForm);

  const data = {
    user_receiver_ids: [formData.get("user")],
    user_requester_id: gameService.user.id,
    game_id: match,
    game_type: VerificationType.GAME,
  };
  wrapperLoadingService.execute(
    authService,
    authService.sendGame2Factor,
    data
  );
}

const submitVerifyForm = async (e) => {
  e.preventDefault();
  const verifyForm = document.getElementById("validation-form");
  const formData = new FormData(verifyForm);

  await gameService.validateGame(match, formData).then(handleValidateResponse);
};

const handleValidateResponse = async (response) => {
  if (typeof response === "string") {
    putVerifyForm(response);
  } else {
    if (response.hasOwnProperty("is_success") && response.is_success === true) {
      window.location.href = "?match=" + match + "#pong";
      return;
    }
  }
  loadErrorMessage(response, "verify-game-container");
};

const start = async (user) => {
  match = new URLSearchParams(window.location.search).get("match");
  if (match === null) {
    pageNotFoundMessage("message");
    return;
  }

  gameService.user = user;
  await gameService.validateGameForm(match).then(putVerifyForm);
};

export default new ValidateGameView(html, start);
