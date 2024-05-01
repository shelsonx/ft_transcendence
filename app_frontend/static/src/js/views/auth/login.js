
import { FormValidation } from '../../contracts/validation/formValidation.js';
import { EmailValidatorInput, RequiredInputValidator } from '../../contracts/validation/validatorInput.js';
import authLocale from '../../locale/auth/authLocale.js';
import authService from '../../services/authService.js';
import wrapperLoadingService from '../../services/wrapperService.js';
import { togglePasswordVisibility } from '../../utils/togglePasswordVisibility.js';
import BaseAuthView from './baseAuthView.js';
class LoginView extends BaseAuthView {
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
            <h2>Login</h2>
            <p id="selected-language"></p>
            <form id="login-form" class="auth-form d-flex flex-column gap-2 g-lg-0" novalidate>
                <div>
                    <label for="email">Email</label>
                    <div class="input-group input-group-custom">
                        <input class="form-control" type="email" id="email" name="email" required>
                    </div>
                </div>
                <div>
                    <label for="password">Password</label>
                    <div class="input-group input-group-custom position-relative">
                        <input class="form-control" type="password" id="password" name="password" required>
                        <span class="input-group-text cursor-pointer">
                            <i id="show-password-icon" class="bi bi-eye-slash"></i>
                        </span>
                    </div>
                </div>
                <a id="forgot-password-link" href="#forgot-password" class="text-warning p-2 rounded-1 cursor-pointer">Forgot password?</a>
                <div class="ms-auto mt-1">
                    <a href="#sign-up" class="btn btn-secondary">Sign Up</a>
                    <button class="btn btn-primary" type="submit">Login</button>
                </div>
            </form>
            <p class="my-2">Or</p>
            <button 
                class="btn btn-success w-100 m-0 d-flex justify-content-center align-items-center gap-3" 
                type="button"
                id="login-42"
                >
                <span>Login with</span> 
                <img class="button-42" src="static/src/img/42-logo.svg" />
            </button>
        </div>
    </div>
`;

function action() {
    const form = document.getElementById('login-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formValidation = new FormValidation([
            new EmailValidatorInput('email'),
            new RequiredInputValidator('password', "Password"),
        ]);
        if (!formValidation.isValid()) {
            return;
        }
        const formData = new FormData(form);
        const response = await wrapperLoadingService.execute(
            authService,
            authService.login, 
            formData
        );
        console.log(response);
        authService.addTokenToLocalStorage(response)
        authService.redirectIfAuthenticated(response, formData.get('email'));
    });
    const login42 = document.getElementById('login-42');
    login42.addEventListener('click', async () => {
        authService.login42();
    });
    togglePasswordVisibility('password', 'show-password-icon');
    document.getElementById('selected-language').addEventListener('custom:onLanguageChange', (e) => {
        const selectedLanguage = e.detail.language;
        e.target.textContent = authLocale[selectedLanguage]['Login'];
      });
}

export default new LoginView(html, action);

