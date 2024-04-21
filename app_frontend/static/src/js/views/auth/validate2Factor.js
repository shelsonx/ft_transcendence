
import { FormValidation } from '../../contracts/validation/formValidation.js';
import { EmailValidatorInput, TwoFactorCodeValidatorInput } from '../../contracts/validation/validatorInput.js';
import authService from '../../services/authService.js';
import wrapperLoadingService from '../../services/wrapperService.js';
import BaseAuthView from './baseAuthView.js';

class TwoFactorView extends BaseAuthView {
    constructor(html, start) {
        super({ html, start });
    }
}


const html = /*html*/`
    <div class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
        <img class="space-man" src="static/src/img/transcendence-journey.svg" />
        <div class="d-flex flex-column align-items-center justify-content border border-white border-opacity-10 rounded-3 p-4 form-container">
            <h3>Validate 2 Factor Code</h3>
            <form id="validate-2fa-form" class="d-flex flex-column gap-2 g-lg-0 w-100" novalidate>
            <div class="w-100">
                    <label for="email">Email</label>
                    <div class="input-group">
                        <input class="form-control" type="email" id="email" name="email" disabled>
                    </div>
                </div>
                <div class="w-100">
                    <label for="two-factor-code">Two Factor Code</label>
                    <div class="input-group">
                        <input class="form-control" type="number" id="two-factor-code" name="two-factor-code" required>
                    </div>
                </div>
                <div class="ms-auto mt-1">
                    <button id="resend-2fa" class="btn btn-secondary" type="button">Resend 2FA Code</button>
                    <button class="btn btn-primary" type="submit">Submit</button>
                </div>
            </form>
        </div>
`;

function start() {
  const email = new URLSearchParams(window.location.search).get('email');
  document.getElementById('email').value = email;
  
  const form = document.getElementById('validate-2fa-form');
  form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formValidation = new FormValidation([
          new EmailValidatorInput('email'),
          new TwoFactorCodeValidatorInput('two-factor-code'),
      ]);
      if (!formValidation.isValid()) {
          return;
      }
      const formData = new FormData(form);
      formData.set('email', email);
      const response = await wrapperLoadingService.execute(
          authService,
          authService.validateTwoFactorCode, 
          formData
      );
      console.log(response);
      authService.addTokenToLocalStorage(response)
      authService.redirectIfAuthenticated(response, formData.get('email'));
  });

  const buttonResend = document.getElementById("resend-2fa");
  buttonResend.addEventListener('click', async (e) => {
    e.preventDefault();
    const response = await wrapperLoadingService.execute(
        authService,
        authService.resendTwoFactorCode, 
        email
    );
    console.log(response);
  })

}

export default new TwoFactorView(html, start);
