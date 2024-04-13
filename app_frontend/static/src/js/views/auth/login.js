
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
            <h1>Login</h1>
            <form id="login-form" class="d-flex flex-column gap-2 g-lg-0" novalidate>
                <div>
                    <label for="email">Email</label>
                    <div class="input-group input-group-custom">
                        <input class="form-control" type="email" id="email" name="email" required>
                    </div>
                </div>
                <div>
                    <label for="password">Password</label>
                    <div class="input-group input-group-custom">
                        <input class="form-control" type="password" id="password" name="password" required>
                    </div>
                </div>
                <div class="ms-auto mt-1">
                    <a href="#sign-up" class="btn btn-success">Sign Up</a>
                    <button class="btn btn-primary" type="submit">Login</button>
                </div>

            </form>
        </div>
`;

function action() {
    const form = document.getElementById('login-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formValidation = new FormValidation([
            new EmailValidatorInput('email'),
            new PasswordInputValidator('password'),
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
}





export default new LoginView({ html, start: action });

