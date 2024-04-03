import View from '../contracts/View.js';
class LoginView extends View {
    constructor(html, start) {
        super(html, start);
    }
}

const html = /*html*/`
    <h1>Login</h1>
    <form id="login-form" class="flex flex-column gap-1 g-lg-0">
        <div>
            <label for="username">Email</label>
            <div class="input-group flex flex-nowrap">
                <input class="form-control" type="email" id="email" name="email" required>
            </div>
        </div>
        <div>
            <label for="username">Username</label>
            <div class="input-group flex flex-nowrap">
                <input class="form-control" type="text" id="username" name="username" required>
            </div>
        </div>
        <div>
            <label for="password">Password</label>
            <div class="input-group flex flex-nowrap">
                <input class="form-control" type="password" id="password" name="password" required>
            </div>
        </div>
        <div>
            <label for="confirm-password">Confirm Password</label>
            <div class="input-group flex flex-nowrap">
                <input class="form-control" type="confirm-password" id="confirm-password" name="confirm-password" required>
            </div>
        </div>
        <button class="btn btn-primary" type="submit">Login</button>
    </form>
`;

function action() {
    const form = document.getElementById('login-form');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const data = {
                email: formData.get('email'),
                username: formData.get('username'),
                password: formData.get('password'),
                confirm_password: formData.get('confirm-password')
            }
            console.log(data);
        });
}

export default new LoginView(html, action);

