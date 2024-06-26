import BaseLoggedView from "../baseLoggedView.js";
import authService from "../../services/authService.js";
import gameService from "../../services/gameService.js";
import wrapperLoadingService from '../../services/wrapperService.js';
import { loadErrorMessage, pageNotFoundMessage } from "../../utils/errors.js";
import { VerificationType } from "../../contracts/game/validation.js";
import { isValidToken } from "../../contracts/validation/tokenValidation.js";
import { CustomEvents } from "../../constants/custom-events.js";

class ValidateTournamentView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start,
    });
  }
}

const html = /*html*/ `
  <div class="main-game scroll-on container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
    <div id="verify-tournament-container" class="static"></div>
  </div>
`;

let tournament = null;

const putVerifyTable = async (response) => {
  if (response.status !== undefined) {
    loadErrorMessage(response, "verify-tournament-container");
    return;
  }

  const swapContainer = document.getElementById("verify-tournament-container");
  swapContainer.innerHTML = response;

  const verifyForms = document.querySelectorAll("form");
  verifyForms.forEach((form) => {
    form.addEventListener("submit", submitVerifyForm);
  });

  const resendCodeButtons = document.querySelectorAll(".resend");
  resendCodeButtons.forEach((form) => {
    form.addEventListener("click", resendCode);
  });
};

const resendCode = (e) => {
  e.preventDefault();
  const btn = e.srcElement;
  const player = btn.id.split("-").pop();
  const form = document.getElementById(`validate-${player}`);
  const formData = new FormData(form);

  const data = {
    user_receiver_ids: [formData.get("user")],
    user_requester_id: gameService.user.id,
    game_id: tournament,
    game_type: VerificationType.TOURNAMENT,
  };
  wrapperLoadingService.execute(
    authService,
    authService.sendGame2Factor,
    data
  );
}

const invalidToken = (player) => {
  const errors = document.getElementsByClassName("form-error");
  if (errors.length > 0) {
    [...errors].forEach(errorElement => {
      errorElement.remove();
    });
  }

  const tokenField = document.getElementById(`token-${player}`);
  var errorElement = document.createElement('div');
  errorElement.classList.add("form-error");
  errorElement.classList.add("p-sm");
  errorElement.setAttribute("data-i18n-key", "invalid-access-token");
  errorElement.innerText = "Invalid Access Token";
  tokenField.appendChild(errorElement);
}

const submitVerifyForm = async (e) => {
  e.preventDefault();
  const form = e.srcElement;
  const player = form.id.split("-").pop();
  const formData = new FormData(form);
  const token = formData.get("token");
  if (!isValidToken(token)) return invalidToken(player);

  await gameService
    .validateTournament(tournament, player, formData)
    .then(verifyPlayerResult);
};

const verifyPlayerResult = async (response) => {
  if (typeof response === "string") {
    putVerifyTable(response);
  } else {
    if (response.hasOwnProperty("is_success") && response.is_success === true) {
      window.location.href = "?t=" + tournament + "#tournament";
      return;
    }
  }
  loadErrorMessage(response, "verify-tournament-container");
};

const start = async (user) => {
  tournament = new URLSearchParams(window.location.search).get("t");
  if (tournament === null) {
    pageNotFoundMessage("message");
    return;
  }

  gameService.user = user;
  await gameService.validateTournamentForm(tournament).then(putVerifyTable);

  window.addEventListener(CustomEvents.LANGUAGE_CHANGE_EVENT, async (e) => {
    await gameService.validateTournamentForm(tournament).then(putVerifyTable);
  });
};

export default new ValidateTournamentView(html, start);
