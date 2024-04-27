

import { FormValidation } from '../../contracts/validation/formValidation.js';
import { ConfirmPasswordInputValidator, EmailValidatorInput, PasswordInputValidator, UsernameValidatorInput } from '../../contracts/validation/validatorInput.js';
import authService from '../../services/authService.js';
import wrapperLoadingService from '../../services/wrapperService.js';
import { togglePasswordVisibility } from '../../utils/togglePasswordVisibility.js';
import BaseAuthView from './baseAuthView.js';

class SignUpView extends BaseAuthView {
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
            <h1>Sign Up</h1>
            <form id="signup-form" class="d-flex flex-column gap-2 g-lg-0" novalidate>
                <div>
                    <label for="email">Email</label>
                    <div class="input-group input-group-custom">
                        <input class="form-control" type="email" id="email" name="email" required>
                    </div>
                </div>
                <div>
                    <label for="username">User Name</label>
                    <div class="input-group input-group-custom">
                        <input class="form-control" type="text" id="username" name="username" required>
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
                <div>
                    <label for="confirm-password">Confirm Password</label>
                    <div class="input-group input-group-custom position-relative">
                        <input class="form-control" type="password" id="confirm-password" name="confirm-password" required>
                        <span class="input-group-text cursor-pointer">
                            <i id="show-confirm-password-icon" class="bi bi-eye-slash"></i>
                        </span>
                    </div>
                </div>
                <div class="ms-auto mt-1">
                    <a href="#login" class="btn btn-secondary">Sign In</a>
                    <button class="btn btn-primary" type="submit">Sign Up</button>
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

function start() {
    const form = document.getElementById('signup-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formValidation = new FormValidation([
            new PasswordInputValidator('password'),
            new EmailValidatorInput('email'),
            new ConfirmPasswordInputValidator('confirm-password', 'password'),
            new UsernameValidatorInput('username')

        ]);
        if (!formValidation.isValid()) {
            return;
        }
        const formData = new FormData(form);
        const response = await wrapperLoadingService.execute(
            authService,
            authService.register,
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
    togglePasswordVisibility('confirm-password', 'show-confirm-password-icon');
}

export default new SignUpView(html, start);

