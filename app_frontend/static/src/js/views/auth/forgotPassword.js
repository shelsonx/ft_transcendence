
import { FormValidation } from '../../contracts/validation/formValidation.js';
import { ConfirmPasswordInputValidator, EmailValidatorInput, PasswordInputValidator, TwoFactorCodeValidatorInput } from '../../contracts/validation/validatorInput.js';
import authService from '../../services/authService.js';
import wrapperLoadingService from '../../services/wrapperService.js';
import { togglePasswordVisibility } from '../../utils/togglePasswordVisibility.js';
import BaseAuthView from './baseAuthView.js';

class ForgotPassword extends BaseAuthView {
    constructor(html, start) {
        super({
            html, start
        });
    }
}


const html = /*html*/`
    <div class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
        <img class="space-man" src="static/src/img/transcendence-journey.svg" />
        <div class="d-flex flex-column align-items-center justify-content border border-white border-opacity-10 rounded-3 p-4 form-container">
            <h3
              data-i18n-key="auth--forgot-password"
            >Forgot Password</h3>
            <form id="forgot-password-form" class="auth-form d-flex flex-column gap-2 g-lg-0 w-100" novalidate>
                <div>
                    <label for="email">Email</label>
                    <div class="input-group input-group-custom">
                        <input class="form-control" type="email" id="email" name="email">
                    </div>
                </div>
                <div class="d-none">
                    <label for="two-factor-code"
                    data-i18n-key="two-factor-auth--two-factor-code"
                    >Two Factor Code</label>
                    <div class="input-group input-group-custom">
                        <input class="form-control" type="number" id="two-factor-code" name="two-factor-code" required>
                    </div>
                </div>
                <div class="d-none">
                    <label for="password"
                    data-i18n-key="auth--password"
                    >Password</label>
                    <div class="input-group input-group-custom position-relative">
                        <input class="form-control" type="password" id="password" name="password" required>
                        <span class="input-group-text cursor-pointer">
                            <i id="show-password-icon" class="bi bi-eye-slash"></i>
                        </span>
                    </div>
                </div>
                <div class="d-none">
                    <label for="confirm-password"
                    data-i18n-key="auth--confirm-password"
                    >Confirm Password</label>
                    <div class="input-group input-group-custom position-relative">
                        <input class="form-control" type="password" id="confirm-password" name="confirm-password" required>
                        <span class="input-group-text cursor-pointer">
                            <i id="show-confirm-password-icon" class="bi bi-eye-slash"></i>
                        </span>
                    </div>
                </div>
                <div class="ms-auto mt-1 d-flex gap-2">
                    <button id="resend-2fa" class="btn btn-secondary reduce-font-size" type="button"
                      data-i18n-key="two-factor-auth--resend"
                    >Resend code</button>
                    <button class="btn btn-primary d-none reduce-font-size" type="submit"
                      data-i18n-key="two-factor-auth--submit"
                    >Submit</button>
                </div>
            </form>
        </div>
`;

function start() {
  const form = document.getElementById('forgot-password-form');
  form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formValidation = new FormValidation([
          new EmailValidatorInput('email'),
          new TwoFactorCodeValidatorInput('two-factor-code'),
          new PasswordInputValidator('password'),
          new ConfirmPasswordInputValidator('confirm-password', 'password'),
        ]);
      if (!formValidation.isValid()) {
          return;
      }
      const formData = new FormData(form);
      const response = await wrapperLoadingService.execute(
          authService,
          authService.forgotPassword,
          formData
      );
      authService.addTokenToLocalStorage(response)
      authService.redirectIfAuthenticated(response, formData.get('email'));
  });

  const buttonResend = document.getElementById("resend-2fa");
  buttonResend.addEventListener('click', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const formValidation = new FormValidation([new EmailValidatorInput('email')]);
    if (!formValidation.isValid()) {
        return;
    }
    const response = await wrapperLoadingService.execute(
        authService,
        authService.resendTwoFactorCode,
        email
    );
    if (response.is_success) {
      const getDisplayNoneElements = document.querySelectorAll('.d-none');
      getDisplayNoneElements.forEach(element => {
        element.classList.remove('d-none');
      });
    }
  })

  togglePasswordVisibility('password', 'show-password-icon');
  togglePasswordVisibility('confirm-password', 'show-confirm-password-icon');

}

export default new ForgotPassword( html, start );
