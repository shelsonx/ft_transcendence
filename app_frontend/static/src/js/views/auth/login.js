
import authService from '../../services/authService.js';
import BaseAuthView from './baseAuthView.js';
class LoginView extends BaseAuthView {
    constructor(html, start) {
        super(html, start);
    }
}

const html = /*html*/`
    <div class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
        <div class="space-man-container"></div>
        <div class="d-flex flex-column align-items-center justify-content border border-white border-opacity-10 rounded-3 p-4 form-container">
            <h1>Login</h1>
            <form id="login-form" class="d-flex flex-column gap-2 g-lg-0">
                <div>
                    <label for="email">Email</label>
                    <div class="input-group d-flex flex-nowrap">
                        <input class="form-control" type="email" id="email" name="email" required>
                    </div>
                </div>
                <div>
                    <label for="password">Password</label>
                    <div class="input-group d-flex flex-nowrap">
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
        const formData = new FormData(form);
        const response = await authService.login(formData);
        console.log(response);
    });
}



export default new LoginView({ html, start: action });

