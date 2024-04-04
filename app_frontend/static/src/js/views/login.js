import View from '../contracts/view.js';
class LoginView extends View {
    constructor(html, start) {
        super(html, start);
    }
}

const html = /*html*/`
    <h1>Login</h1>
    <form id="login-form" class="flex flex-column gap-1 g-lg-0">
        <div>
            <label for="email">Email</label>
            <div class="input-group flex flex-nowrap">
                <input class="form-control" type="email" id="email" name="email" required>
            </div>
        </div>
        <div>
            <label for="user_name">Username</label>
            <div class="input-group flex flex-nowrap">
                <input class="form-control" type="text" id="user_name" name="user_name" required>
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
                user_name: formData.get('user_name'),
                password: formData.get('password'),
                confirm_password: formData.get('confirm-password')
            }
            const response = await fetch('http://localhost:8002/api/auth/sign-up/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            const json = await response.json();
            console.log(json);
        });
}

export default new LoginView(html, action);

