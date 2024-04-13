

import { FormValidation } from '../../contracts/validation/formValidation.js';
import { EmailValidatorInput, PasswordInputValidator } from '../../contracts/validation/validatorInput.js';
import authService from '../../services/authService.js';
import wrapperLoadingService from '../../services/wrapperService.js';
import BaseAuthView from './baseAuthView.js';

class LoginView extends BaseAuthView {
    constructor(html, start) {
        super(html, start);
    }
}

const html = /*html*/`
    <div class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
        <img class="space-man" src="static/src/img/transcendence-journey.svg" />
        <div class="d-flex flex-column align-items-center justify-content border border-white border-opacity-10 rounded-3 p-4 form-container">
            <h1>Sign Up</h1>
            <form id="signup-form" class="d-flex flex-column gap-2 g-lg-0">
                <div>
                    <label for="email">Email</label>
                    <div class="input-group d-flex flex-nowrap">
                        <input class="form-control" type="email" id="email" name="email" required>
                    </div>
                </div>
                <div>
                    <label for="username">User Name</label>
                    <div class="input-group d-flex flex-nowrap">
                        <input class="form-control" type="text" id="username" name="username" required>
                    </div>
                </div>
                <div>
                    <label for="password">Password</label>
                    <div class="input-group d-flex flex-nowrap">
                        <input class="form-control" type="password" id="password" name="password" required>
                    </div>
                </div>
                <div>
                    <label for="confirm-password">Confirm Password</label>
                    <div class="input-group d-flex flex-nowrap">
                        <input class="form-control" type="password" id="confirm-password" name="confirm-password" required>
                    </div>
                </div>
                <div class="ms-auto mt-1">
                    <a href="#login" class="btn btn-success">Sign In</a>
                    <button class="btn btn-primary" type="submit">Sign Up</button>
                </div>

            </form>
        </div>
    </div>
`;

function start() {
    const form = document.getElementById('signup-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formValidation = new FormValidation([
            new PasswordInputValidator('password'),
            new EmailValidatorInput('email')
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
}

export default new LoginView({ html, start });

