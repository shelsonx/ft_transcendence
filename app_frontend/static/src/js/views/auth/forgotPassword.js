
import { FormValidation } from '../../contracts/validation/formValidation.js';
import { ConfirmPasswordInputValidator, EmailValidatorInput, PasswordInputValidator, TwoFactorCodeValidatorInput } from '../../contracts/validation/validatorInput.js';
import authService from '../../services/authService.js';
import wrapperLoadingService from '../../services/wrapperService.js';
import { togglePasswordVisibility } from '../../utils/togglePasswordVisibility.js';
import BaseAuthView from './baseAuthView.js';

class ForgotPassword extends BaseAuthView {
    constructor(html, start) {
        super(html, start);
    }
}


const html = /*html*/`
    <div class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
        <img class="space-man" src="static/src/img/transcendence-journey.svg" />
        <div class="d-flex flex-column align-items-center justify-content border border-white border-opacity-10 rounded-3 p-4 form-container">
            <h3>Forgot Password</h3>
            <form id="forgot-password-form" class="d-flex flex-column gap-2 g-lg-0 w-100" novalidate>
                <div class="w-100">
                    <label for="email">Email</label>
                    <div class="input-group">
                        <input class="form-control" type="email" id="email" name="email">
                    </div>
                </div>
                <div class="w-100 d-none">
                    <label for="two-factor-code">Two Factor Code</label>
                    <div class="input-group">
                        <input class="form-control" type="number" id="two-factor-code" name="two-factor-code" required>
                    </div>
                </div>
                <div class="d-none">
                    <label for="password">Password</label>
                    <div class="input-group input-group-custom position-relative">
                        <input class="form-control" type="password" id="password" name="password" required>
                        <i id="show-password-icon" class="bi bi-eye-slash position-absolute top-50 end-0 translate-middle-y text-secondary p-2 cursor-pointer z-999"></i>
                    </div>
                </div>
                <div class="d-none">
                    <label for="confirm-password">Confirm Password</label>
                    <div class="input-group input-group-custom position-relative">
                        <input class="form-control" type="password" id="confirm-password" name="confirm-password" required>
                        <i id="show-confirm-password-icon" class="bi bi-eye-slash position-absolute top-50 end-0 translate-middle-y text-secondary p-2 cursor-pointer z-999"></i>
                    </div>
                </div>
                <div class="ms-auto mt-1">
                    <button id="resend-2fa" class="btn btn-secondary" type="button">Send 2FA Code</button>
                    <button class="btn btn-primary d-none" type="submit">Submit</button>
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
      console.log(response);
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
    console.log(response);
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

export default new ForgotPassword({ html, start });
